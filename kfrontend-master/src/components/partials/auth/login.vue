<template>
	<form class="w-full sm:w-[368px] px-4 sm:px-0 mx-auto" @submit.prevent="login">
		<div v-show="props.showRegister" class="mt-8 ml-2">
			<i18n-t keypath="no_account.pre" tag="p" class="text-xs text-gray-400">
				<button
					type="button"
					class="rounded font-medium text-primary hover:text-primary-light focus:outline-none focus:ring-primary-light focus:ring-2 active:text-primary-dark"
					@click="router.push({ name: 'Register' })">
					{{ t("no_account.link") }}
				</button>
			</i18n-t>
		</div>

		<CustomInput
			class="mt-2"
			:label="t('username.title')"
			type="text"
			:name="'username'"
			:option-selected="state.username"
			:error="v$.username.$errors.length == 0 ? '' : v$.username.$errors[0].$message"
			@value-changed="(option) => (state.username = option)" />

		<CustomInput
			class="mt-8"
			:label="t('password.title')"
			type="password"
			:name="'password'"
			:option-selected="state.password"
			:error="v$.password.$errors.length == 0 ? '' : v$.password.$errors[0].$message"
			@value-changed="(option) => (state.password = option)" />

		<div class="ml-auto max-w-max mr-2">
			<button
				type="button"
				class="rounded font-medium text-xs text-gray-400 hover:text-gray-300 focus:outline-none focus:ring-gray-300 focus:ring-2 active:text-gray-500"
				@click="router.push({ name: 'Forgot Password' })">
				{{ t("password.forgot") }}
			</button>
		</div>

		<div class="relative mt-16">
			<Button
				:message="t('sign_in.button')"
				:loading="showSpinningWheel"
				:show-x="showX"
				:show-check="showCheck"
				:pill="true"
				type="primary"
				:submit="true" />
		</div>
	</form>
</template>
<script setup>
import Button from "@/components/partials/button.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import authorizationService from "@/services/authorization.service";
import store from "@/store";
import router from "@/router";
import { required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	showRegister: {
		required: false,
		type: Boolean,
		default: true,
	},
	email: {
		required: false,
		type: String,
		default: "",
	},
});

const emit = defineEmits(["loginOk"]);

const maxLen = helpers.withMessage(t("errors.maxLen", { count: 255 }), maxLength(255));
const maxLen2 = helpers.withMessage(t("errors.maxLen", { count: 100 }), maxLength(100));

let state = ref({
	username: props.email,
	password: "",
});

let rules = {
	username: {
		required: helpers.withMessage(t("errors.required"), required),
		max: maxLen2,
	},
	password: {
		required: helpers.withMessage(t("errors.required"), required),
		max: maxLen,
	},
};

let v$ = useVuelidate(rules, state);
let showSpinningWheel = ref(false);
let showCheck = ref(false);
let showX = ref(false);

async function login() {
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		return;
	}
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	let promise = new Promise((resolve) => setTimeout(resolve, 1000));
	let post = authorizationService.doLogin(state.value.username, state.value.password);

	Promise.all([post, promise])
		.then(() => {
			// Guarda o current user na store
			authApi.get("users/me").then((response) => {
				showSpinningWheel.value = false;
				showCheck.value = true;
				store.commit("setUser", response.data);
				setTimeout(function () {
					emit("loginOk");
				}, 1000);
			});
		})
		.catch((error) => {
			showSpinningWheel.value = false;
			showX.value = true;
			console.log(error);
			if (error?.response?.status === 403) {
				if (error.response.data.detail == "Email Not Verified") {
					router.push({ name: "Verify Email" });
					return;
				}
				if (error.response.data.detail == "User Blocked") {
					router.push({ name: "Block" });
					return;
				}
				if (error.response.data.detail == "Admin Not Verified") {
					router.push({ name: "Verify Admin", params: { refuse: "false" } });
					return;
				}
				if (error.response.data.detail == "Admin Refuse") {
					router.push({ name: "Verify Admin", params: { refuse: "true" } });
					return;
				}
			}
			errorHandling(error);
		});
}
</script>

<i18n>
{
	"en_GB": {
		"sign_in": {
			"title": "Sign in",
			"button": "Sign in"
		},
		"username": {
			"title": "Email address",
			"placeholder": "Enter your email address",
			"notVerified": "Email not Verified"
		},
		"password": {
			"title": "Password",
			"placeholder": "Enter your secret password",
			"forgot": "Forgot your password?"
		},
		"no_account": {
			"pre": "Don't have an account? {0}",
			"link": "Sign up"
		},
		"errors": {
			"required": "Cannot be empty",
			"emailInvalid": "The email is not valid",
			"maxLen": "The max length is {count} characters",
			"verify": {
				"email": "You need to validate your email first"
			},
			"userBlocked": "User Blocked"
		}
	},
	"pt_PT": {
		"sign_in": {
			"title": "Iniciar sessão",
			"button": "Entrar"
		},
		"email": {
			"title": "Endereço de email",
			"placeholder": "Insira o seu endereço de email",
			"notVerified": "Email não verificado"
		},
		"password": {
			"title": "Palavra-chave",
			"placeholder": "Insira a sua palavra-cahve",
			"forgot": "Esqueceu-se da sua palavra-chave?"
		},
		"no_account": {
			"pre": "Não possui uma conta? {0}",
			"link": "Increva-se"
		},
		"errors": {
			"required": "Não pode estar vazio",
			"emailInvalid": "O endereço de email não é válido",
			"maxLen": "No máximo só pode ter {count} caratéres",
			"verify": {
				"email": "É necessário que confirme o seu email primeiro"
			},
			"userBlocked": "Utilizador bloqueado"
		}
	}
}
</i18n>
