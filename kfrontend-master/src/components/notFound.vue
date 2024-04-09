<template>
	<div class="w-full text-center text-2xl font-bold mt-20">
		{{ t("title") }}
	</div>
	<router-link :to="{ name: 'Root' }" class="button max-w-lg w-full mx-auto mt-5">
		{{ t("home") }}
	</router-link>
</template>

<script setup>
import { useI18n } from "vue-i18n";

let { t } = useI18n();
</script>

<i18n>
{
  "en_GB": {
    "title": "Sorry but looks like the page you are looking for doesn't exist",
    "home": "Go to the home page"
  },
  "pt_PT": {
    "title": "Pedimos desculpa mas parece que a página que procura não existe",
    "home": "Ir para a página inicial"
  }
}
</i18n>
