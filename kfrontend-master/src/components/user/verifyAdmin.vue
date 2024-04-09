<template>
	<AuthenticationTemplate :title="props.refuse == 'true' ? t('title.failed') : t('title.await')">
		<div v-if="props.refuse == 'true'">
			<p class="text-center font-medium text-lg">
				{{ t("failed") }}
			</p>
		</div>
		<div v-else class="text-center font-medium text-lg">
			<p>
				{{ t("awaiting.first") }}
			</p>
			<p>{{ t("awaiting.second") }}</p>
		</div>
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import store from "@/store";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

const props = defineProps({
	refuse: {
		required: true,
		type: String,
	},
});
</script>

<i18n>
{
    "en_GB": {
        "title": {
            "await": "Waiting Admin Verification",
            "failed": "Admin Verification Failed"
        },
        "failed": "Your account was denied access by one of our administrators, if you believe this is an error please contact us at: ",
        "awaiting": {
            "first": "Your account is in waiting list to being verified, after that you can access the website as normal.",
            "second": "Once your account is verified an email will be sent to you."
        }
    },
    "pt_PT": {
        "title": {
            "await": "À espera de verificação do administrador",
            "failed": "Verificação do administrador falhou"
        },
        "failed": "A sua conta foi bloqueada por um administrador, se acredita que isto é um erro por favor contacte-nos em: ",
        "awaiting": {
            "first": "A sua conta encontra-se na lista de espera para ser verificada, assim que esta for verificada poderá aceder ao website como normal.",
            "second": "Uma vez que a sua conta seja verificada um email ser-lhe-á enviado."
        }
    }
}
</i18n>
