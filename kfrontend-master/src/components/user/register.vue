<template>
	<AuthenticationTemplate :title="t('title')">
		<Register @register-ok="router.push({ name: 'Verify Email' })" />
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import Register from "@/components/partials/auth/register.vue";
import store from "@/store";
import router from "@/router";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);
</script>

<i18n>
{
  "en_GB": {
    "title": "Sign up"
  },
  "pt_PT": {
    "title": "Criar uma nova conta"
  }
}
</i18n>
