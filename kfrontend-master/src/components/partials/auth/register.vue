<template>
	<form class="w-full sm:w-[368px] mx-auto" @submit.prevent="register">
		<div class="inline-flex space-x-8 mt-8">
			<CustomInput
				:label="t('name.title.first')"
				type="text"
				:name="'firstName'"
				:option-selected="state.firstName"
				:error="v$.firstName.$errors.length == 0 ? '' : v$.firstName.$errors[0].$message"
				@value-changed="(option) => (state.firstName = option)" />
			<CustomInput
				:label="t('name.title.last')"
				type="text"
				:name="'lastName'"
				:option-selected="state.lastName"
				:error="v$.lastName.$errors.length == 0 ? '' : v$.lastName.$errors[0].$message"
				@value-changed="(option) => (state.lastName = option)" />
		</div>
		<div class="mt-8">
			<CustomInput
				:label="t('email.title')"
				type="text"
				:name="'email'"
				:option-selected="state.email"
				:readonly="props.readonlyEmail"
				:error="v$.email.$errors.length == 0 ? '' : v$.email.$errors[0].$message"
				@value-changed="(option) => (state.email = option)" />
		</div>
		<div class="mt-8">
			<CustomInput
				:label="t('password.title')"
				type="password"
				:name="'password'"
				:option-selected="state.password"
				:error="v$.password.$errors.length == 0 ? '' : v$.password.$errors[0].$message"
				@value-changed="(option) => (state.password = option)" />
		</div>
		<div class="mt-8">
			<CustomInput
				:label="t('confirmPassword.title')"
				type="password"
				:name="'confirmPassword'"
				:option-selected="state.confirmPassword"
				:error="
					v$.confirmPassword.$errors.length == 0
						? ''
						: v$.confirmPassword.$errors[0].$message
				"
				@value-changed="(option) => (state.confirmPassword = option)" />
		</div>

		<div v-show="showLogin" class="mt-2">
			<i18n-t keypath="account.pre" tag="p" class="text-xs text-gray-400">
				<button
					class="rounded font-medium text-primary hover:text-primary-light focus:outline-none focus:ring-primary-light focus:ring-2 active:text-primary-dark"
					@click="router.push({ name: 'Login' })">
					{{ t("account.link") }}
				</button>
			</i18n-t>
		</div>

		<div class="relative mt-16 w-full">
			<Button
				:message="t('signUp.button')"
				type="primary"
				:submit="true"
				:pill="true"
				:loading="showSpinningWheel"
				:show-x="showX"
				:show-check="showCheck" />
		</div>
	</form>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref } from "vue";
import router from "@/router";
import toast, { genericError } from "@/toast.js";
import { unauthApi, authApi } from "@/services/api";
import authorizationService from "@/services/authorization.service";
import store from "@/store";
import c from "country-list";
import e from "countries-list";
import { email, required, minLength, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useI18n } from "vue-i18n";

const props = defineProps({
	showLogin: {
		required: false,
		type: Boolean,
		default: true,
	},
	defaultValues: {
		required: false,
		type: Object,
		default: () => {
			return {
				firstName: "",
				lastName: "",
				email: "",
				country: "",
			};
		},
	},
	readonlyEmail: {
		required: false,
		type: Boolean,
		default: false,
	},
	doLogin: {
		required: false,
		type: Boolean,
		default: false,
	},
});

const emit = defineEmits(["registerOk"]);

let { t } = useI18n();

let showSpinningWheel = ref(false);
let showCheck = ref(false);
let showX = ref(false);

let n = c.getCodeList();
let keys = Object.keys(n);
let optionsList = ref([]);
let countries = ref([]);

let state = ref({
	fistName: props.defaultValues.name,
	lastName: props.defaultValues.name,
	email: props.defaultValues.email,
	password: "",
	confirmPassword: "",
});

keys.forEach((key) => {
	optionsList.value.push({
		id: key.toUpperCase(),
		name: e.getEmojiFlag(key.toUpperCase()) + " " + n[key],
	});
});
countries.value = optionsList.value;

const sameAsPassword = (value) => value === state.value.password;
const req = helpers.withMessage(t("errors.required"), required);
const maxLen = helpers.withMessage(t("errors.maxLen", { count: 255 }), maxLength(255));
const maxLen2 = helpers.withMessage(t("errors.maxLen", { count: 100 }), maxLength(100));

let rules = {
	firstName: {
		required: req,
		max: maxLen,
	},
	lastName: {
		required: req,
		max: maxLen,
	},
	email: {
		required: req,
		email: helpers.withMessage(t("errors.emailInvalid"), email),
		max: maxLen2,
	},
	password: {
		required: req,
		minLength: helpers.withMessage(
			() => t("errors.shortPassword", { length: 3 }),
			minLength(3)
		),
		max: maxLen,
	},
	confirmPassword: {
		required: req,
		sameAs: helpers.withMessage(t("errors.differentPasswords"), sameAsPassword),
	},
};

let v$ = useVuelidate(rules, state);
let errorMessage = "";

// Realiza o registo e login do utilizador
async function register() {
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		return;
	}

	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	let payload = {
		name: state.value.firstName.trim() + " " + state.value.lastName.trim(),
		email: state.value.email,
		password: state.value.password,
	};

	// Registar o utilizador
	let post = unauthApi
		.post("auth/register", payload)
		.then((response) => {
			return response.data;
		})
		.catch((error) => {
			errorMessage = error;
			return false;
		});
	let promise = new Promise((resolve) => setTimeout(resolve, 1000));

	Promise.all([post, promise]).then((list) => {
		if (list[0]) {
			if (props.doLogin) {
				unauthApi
					.put("auth/confirms/" + list[0].id)
					.then(() => {
						authorizationService
							.doLogin(state.value.email, state.value.password)
							.then(() => {
								authApi.get("users/me").then((response) => {
									showSpinningWheel.value = false;
									showCheck.value = true;
									store.commit("setUser", response.data);
									setTimeout(function () {
										emit("registerOk");
									}, 1000);
								});
							})
							.catch((error) => {
								showSpinningWheel.value = false;
								showX.value = true;
								errorMessage = error;
								return false;
							});
					})
					.catch((error) => {
						showSpinningWheel.value = false;
						showX.value = true;
						errorMessage = error;
						return false;
					});
			} else {
				setTimeout(function () {
					emit("registerOk");
				}, 1000);
			}
		} else {
			showSpinningWheel.value = false;
			showX.value = true;
			if (
				errorMessage?.response?.data?.detail == undefined ||
				errorMessage?.response?.data?.detail == null
			) {
				genericError();
				return;
			}
			for (let err in errorMessage.response.data) {
				toast.error(errorMessage.response.data[err]);
			}
		}
	});
}
</script>

<i18n>
{
	"en_GB": {
		"signUp": {
			"button": "Sign up"
		},
		"name": {
			"title": {
				"first": "First Name",
				"last": "Last Name"
			},
			"placeholder": "Enter your name",
		},
		"email": {
			"title": "Email address",
			"placeholder": "Enter your email address",
		},
		"password": {
			"title": "Password",
			"placeholder": "Enter your secret password"
		},
		"confirmPassword": {
			"title": "Confirm your Password",
			"placeholder": "Enter your secret password again"
		},
		"country": {
			"title": "Country",
			"placeholder": "Select your country"
		},
		"account": {
			"pre": "Already have an account? {0}",
			"link": "Sign in"
		},
		"errors": {
			"required": "Cannot be empty",
			"emailInvalid": "The email is not valid",
			"shortPassword": "The password must be at least {length} characters long",
			"differentPasswords": "The passwords must match",
			"maxLen": "The max length is {count} characters"
		}
	},
	"pt_PT": {
		"signUp": {
			"button": "Registar"
		},
		"name": {
			"title":  {
				"first": "Primeiro Nome",
				"last": "Último Nome"
			},
			"placeholder": "Insira o seu nome",
		},
		"email": {
			"title": "Endereço de email",
			"placeholder": "Insira o seu endereço de email",
		},
		"password": {
			"title": "Palavra-chave",
			"placeholder": "Insira a sua palavra-chave"
		},
		"confirmPassword": {
			"title": "Confirme a palavra-chave",
			"placeholder": "Insira a sua palavra-chave de novo"
		},
		"account": {
			"pre": "Já possui uma conta? {0}",
			"link": "Entre"
		},
		"errors": {
			"required": "Não pode estar vazio",
			"emailInvalid": "O endereço de email não é válido",
			"shortPassword": "A palavra-chave necessita de pelo menos {length} carateres",
			"differentPasswords": "As palavras-chave precisam de coincidir",
			"maxLen": "No máximo só pode ter {count} caratéres"
		}
	}
}
</i18n>
