<template>
	<div v-if="loadedUser" class="min-h-screen relative">
		<NavBar>
			<router-view />
		</NavBar>
	</div>
</template>

<script setup>
import NavBar from "@/components/partials/navBar.vue";
import { watch } from "vue";
import store from "@/store";
import router from "@/router";
import localStorageService from "@/services/localStorage.service";
import { ref } from "vue";
import authorizationService from "@/services/authorization.service";
import { useI18n } from "vue-i18n";

let { locale } = useI18n();
locale.value = localStorage.getItem("local-language") || "en_GB";
// Saves the last page visited in the store
watch(
	() => router.currentRoute.value.name,
	(to, from) => {
		store.commit("setLastView", from);
		store.commit("setShowNavBar", true);
		store.commit("setShowMargins", true);
	}
);
let loadedUser = ref(false);

authorizationService
	.refreshToken()
	.catch(() => {
		localStorageService.clearTokens();
		store.commit("setUser", null);
	})
	.finally(() => {
		loadedUser.value = true;
	});
</script>
