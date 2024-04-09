<template>
	<AuthenticationTemplate :title="t('title')">
		<div v-if="props.userId == ''" class="max-w-xl m-auto md:col-span-2 lg:col-span-1">
			<p class="font-bold text-xl">
				{{ t("noEmail") }}
			</p>
			<p class="text-lg">
				{{ t("solutions") }}
			</p>

			<CustomInput
				:label="t('email.title')"
				type="text"
				:name="'email'"
				:option-selected="state.email"
				:error="v$.email.$errors.length == 0 ? '' : v$.email.$errors[0].$message"
				@value-changed="(option) => (state.email = option)" />

			<div class="relative mt-16">
				<Button
					:message="t('button')"
					type="primary"
					:pill="true"
					@button-click="resendEmail" />
			</div>
		</div>
		<div v-else>
			<div
				v-if="emailVerified"
				class="mt-8 max-w-xl mx-auto text-center font-semibold text-2xl">
				<p>
					{{ t("verified") }}
				</p>
			</div>
			<div v-else class="max-w-xl mx-auto text-center font-semibold text-2xl">
				<p class="relative top-1/4">
					{{ alreadyVerfied ? t("already") : t("verifying") }}
				</p>
			</div>
			<div
				class="bg-gray-200 rounded-full overflow-hidden mt-20 w-2/3 relative left-1/2 -translate-x-1/2">
				<div
					id="progressBar"
					class="h-2 bg-primary-800 rounded-full transfrom duration-[4000ms] w-0" />
			</div>
		</div>
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import Button from "@/components/partials/button.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { unauthApi } from "@/services/api";
import { ref } from "vue";
import store from "@/store";
import router from "@/router";
import toast, { genericError } from "@/toast.js";
import { email, required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useI18n } from "vue-i18n";
store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);
let { t } = useI18n();
const props = defineProps({
	// ID do user
	userId: {
		type: String,
		required: false,
		default: "",
	},
});
const maxLen = helpers.withMessage(t("errors.maxLen", { count: 100 }), maxLength(100));
let state = ref({
	email: "",
});
let rules = {
	email: {
		required: helpers.withMessage(t("errors.required"), required),
		email: helpers.withMessage(t("errors.emailInvalid"), email),
		max: maxLen,
	},
};
let v$ = useVuelidate(rules, state);
let emailVerified = ref(false);
let alreadyVerfied = ref(false);
if (props.userId != "") {
	unauthApi
		.put("auth/confirms/" + props.userId)
		.then((response) => {
			if (response.data != null) {
				emailVerified.value = true;
				let progressBar = document.getElementById("progressBar");
				progressBar.classList.add("w-full");
				progressBar.classList.remove("w-0");
				setTimeout(() => router.push({ name: "Login" }), 4000);
			} else {
				genericError();
			}
		})
		.catch((error) => {
			if (error?.response?.data?.detail == null) {
				genericError();
				return;
			}
			if (error.response.status == 409) {
				alreadyVerfied.value = true;
				let progressBar = document.getElementById("progressBar");
				progressBar.classList.add("w-full");
				progressBar.classList.remove("w-0");
				setTimeout(() => router.push({ name: "Login" }), 4000);
				return;
			}
			toast.error(error.response.data.detail);
		});
}
async function resendEmail() {
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		return;
	}
	unauthApi
		.get("auth/confirms/resend/" + state.value.email)
		.then(() => {
			toast.success(t("sended"));
		})
		.catch((error) => {
			if (error?.response?.data?.detail == null) {
				genericError();
				return;
			}
			if (error.response.status == 409) {
				alreadyVerfied.value = true;
				setTimeout(router.push("Login"), 4000);
				return;
			}
			toast.error(error.response.data.detail);
		});
}
</script>
<i18n>
{
    "en_GB": {
        "title": "Email Confirmed",
        "email": {
            "title": "Email"
        },
        "sended": "Email sended",
        "solutions": "Verify your spam folder or resend the email",
        "noEmail": "Didn't receive an email?",
        "button": "Resend confirmation email",
        "verifying": "Your email is being verified",
        "verified": "Your email was verified, you will soon be redirected to the login page",
        "already": "Your email was already verified",
        "errors": {
            "required": "Cannot be empty",
            "emailInvalid": "The email is not valid",
            "maxLen": "The max length is {count} characters"
        }
    },
    "pt_PT": {
        "title": "Confirmar Email",
        "email": {
            "title": "Email"
        },
        "sended": "Email enviado",
        "solutions": "Verifique a sua pasta de spam ou então pode reenviar o email",
        "noEmail": "Não recebeu um email?",
        "button": "Reenviar email de confirmação",
        "verifying": "O seu email está a ser verificado",
        "verified": "O seu email foi verificado, será redirecionado brevemente para a página de login",
        "already": "O seu email já foi verificado",
        "errors": {
            "required": "Não pode estar vazio",
            "emailInvalid": "O endereço de email não é válido",
            "maxLen": "No máximo só pode ter {count} caratéres"
        }
    }
}
</i18n>
