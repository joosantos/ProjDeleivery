<template>
	<AuthenticationTemplate :title="t('title')">
		<div>
			<p class="text-center font-medium text-lg">
				{{ t("block") }}
			</p>
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
        "title": "User Blocked",
        "block": "Your account was blocked by one of our administrators, if you believe this is an error please contact us at: ",
    },
    "pt_PT": {
        "title": "Utilizador Bloqueado",
        "block": "A sua conta foi bloqueada por um administrador, se acredita que isto é um erro por favor contacte-nos em: ",
    }
}
</i18n>
