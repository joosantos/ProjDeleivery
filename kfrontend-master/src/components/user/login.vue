<template>
	<AuthenticationTemplate :title="t('signIn')">
		<Login @login-ok="router.push({ name: 'Home' })" />
	</AuthenticationTemplate>
</template>

<script setup>
import AuthenticationTemplate from "@/components/partials/templates/authentication.vue";
import Login from "@/components/partials/auth/login.vue";
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
    "signIn": "Sign in",
  },
  "pt_PT": {
    "signIn": "Iniciar sessão",
  }
}
</i18n>
