<template>
	<AuthenticationTemplate :title="t('title.page')">
		<div v-if="!done" class="flex flex-col justify-top sm:px-6 lg:px-8">
			<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
				<div class="py-8 px-4 sm:rounded-lg sm:px-10">
					<div class="space-y-6">
						<CustomInput
							:label="t('email.title')"
							type="text"
							:name="'email'"
							:option-selected="state.email"
							:error="
								v$.email.$errors.length == 0 ? '' : v$.email.$errors[0].$message
							"
							@value-changed="(option) => (state.email = option)" />

						<div class="relative top-10">
							<Button
								:message="t('button.recover')"
								:pill="true"
								type="primary"
								@button-click="sendRecoverEmail" />
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-else class="flex flex-col justify-top sm:px-6 lg:px-8">
			<div class="sm:mx-auto sm:w-full sm:mt-12 sm:max-w-md">
				<img class="mx-auto sm:h-24 h-12 w-auto" src="/logo.png" alt="Workflow" />
				<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
					{{ t("title.sent") }}
				</h2>
			</div>

			<div class="mt-12 sm:mx-auto sm:w-full sm:max-w-md justify-center">
				<button type="submit" class="button" @click="done = false">
					{{ t("button.noEmail") }}
				</button>
			</div>
		</div>
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { authApi } from "@/services/api";
import store from "@/store";
import { genericError } from "@/toast.js";
import { useI18n } from "vue-i18n";
import { email, required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

let { t } = useI18n();

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

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
// A var done serve para mostrar o div que informa o utilizador que o email foi enviado
let done = ref(false);

async function sendRecoverEmail() {
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		return;
	}
	authApi
		.post("/auth/forgot-password", { email: state.value.email })
		.then(() => {
			done.value = true;
			state.value.email = "";
		})
		.catch(() => {
			genericError();
		});
}
</script>

<i18n>
{
  "en_GB": {
      "email": {
          "title": "Email address"
      },
      "title": {
            "page": "Recover your password",
          "email": "Enter your email address",
          "sent": "Email sent!"
      },
      "button": {
          "recover": "Recover",
          "noEmail": "I didn't recive an email"
      },
      "errors": {
          "required": "Cannot be empty",
          "emailInvalid": "The email is not valid",
		  "maxLen": "The max length is {count} characters"
      }
  },
  "pt_PT": {
      "email": {
          "title": "Endereço de email",
          "placeholder": "Insira o seu endereço de email"
      },
      "title": {
            "page": "Recuperar a palavra passe",
          "email": "Indique o seu endereço de email",
          "sent": "Email enviado!"
      },
      "button": {
          "recover": "Recuperar",
          "noEmail": "Não recebi um email"
      },
      "errors": {
          "required": "Não pode estar vazio",
          "emailInvalid": "O email não é válido",
		  "maxLen": "No máximo só pode ter {count} caratéres"
      }
  }
}
</i18n>
