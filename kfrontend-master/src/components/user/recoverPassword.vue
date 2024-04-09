<template>
	<AuthenticationTemplate :title="t('title')">
		<div class="flex flex-col justify-top sm:px-6 lg:px-8">
			<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
				<div class="py-8 px-4 sm:rounded-lg sm:px-10">
					<div class="space-y-6">
						<CustomInput
							:label="t('password')"
							type="password"
							:name="'password'"
							:option-selected="state.password"
							:error="
								v$.password.$errors.length == 0
									? ''
									: v$.password.$errors[0].$message
							"
							@value-changed="(option) => (state.password = option)" />
						<CustomInput
							:label="t('passwordConfirm')"
							type="password"
							:name="'passwordConfirm'"
							:option-selected="state.passwordConfirm"
							:error="
								v$.passwordConfirm.$errors.length == 0
									? ''
									: v$.passwordConfirm.$errors[0].$message
							"
							@value-changed="(option) => (state.passwordConfirm = option)" />

						<div>
							<Button
								:message="t('change')"
								:pill="true"
								type="primary"
								@button-click="changePassword" />
						</div>
					</div>
				</div>
			</div>
		</div>
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";
import { required, minLength, helpers } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useRoute } from "vue-router";
import router from "@/router";

let { t } = useI18n();

const route = useRoute();
store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

const sameAsPassword = (value) => value === state.value.password;
const req = helpers.withMessage(t("errors.required"), required);

let state = ref({
	password: "",
	passwordConfirm: "",
});

let rules = {
	password: {
		required: req,
		minLength: helpers.withMessage(
			() => t("errors.shortPassword", { length: 3 }),
			minLength(3)
		),
	},
	passwordConfirm: {
		required: req,
		sameAs: helpers.withMessage(t("errors.differentPasswords"), sameAsPassword),
	},
};

let v$ = useVuelidate(rules, state);

async function changePassword() {
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		return;
	}
	authApi
		.post(`/auth/recover/${route.query.token}`, { password: state.value.password })
		.then(() => {
			state.value.password = "";
			state.value.passwordConfirm = "";
			toast.success(t("updated"));
			router.push({ name: "Login" });
		})
		.catch((e) => {
			errorHandling(e, true);
		});
}
</script>

<i18n>
{
	"en_GB": {
		"password": "Password",
		"passwordConfirm": "Confirm your Password",
		"title": "Change your Password",
		"change": "Change Password",
		"errors": {
			"required": "Cannot be empty",
			"shortPassword": "The password must be at least {length} characters long",
			"differentPasswords": "The passwords must match",
		}
	},
	"pt_PT": {
		"password": "Password",
		"passwordConfirm": "Confirme a sua Password",
		"title": "Altere a sua Password",
		"change": "Alterar Password",
		"errors": {
			"required": "Não pode estar vazio",
			"shortPassword": "The password must be at least {length} characters long",
        	"differentPasswords": "As palavras-chave precisam de coincidir",
		}
	}
}
</i18n>
