<template>
	<div class="flex flex-col p-6 gap-y-2 w-full">
		<div class="text-center text-4xl">
			<span>
				{{ t("welcome") }}
			</span>
			<span v-if="store.getters.getUser?.name" class="font-semibold">{{
				" " + store.getters.getUser?.name
			}}</span>
			<span>!</span>
		</div>
		<br />
		<br />
		<div class="grid grid-cols-4 justify-center">
			<router-link :to="{ name: 'Competition' }" class="col-start-2 mx-auto max-w-max">
				<BuildingLibraryIcon class="h-40 mx-auto" />
				<p class="font-medium text-3xl text-center capitalize">
					{{ t("showCompetitions") }}
				</p>
			</router-link>
			<router-link :to="{ name: 'Global Statistics' }" class="mx-auto max-w-max">
				<PodiumIcon class="h-40 w-40 mx-auto" />
				<p class="font-medium text-3xl text-center capitalize">
					{{ t("showAthletesStatistics") }}
				</p>
			</router-link>
		</div>
	</div>
</template>

<script setup>
import { BuildingLibraryIcon } from "@heroicons/vue/24/solid";
import PodiumIcon from "@/components/icons/podium.vue";
import store from "@/store";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });
</script>
