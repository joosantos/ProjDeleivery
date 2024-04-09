<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<!-- Title -->
		<div class="font-semibold text-3xl text-center mt-2">
			{{ competition.name }}
		</div>

		<!-- Link to athletes numbers -->
		<div class="ml-auto max-w-max">
			<router-link
				v-if="store.getters.getUserRole == 'ADMIN'"
				:to="{
					name: 'Statistics Athletes Numbers',
					params: { competitionId: props.competition },
				}">
				<Button
					class="max-w-max"
					:message="t('showAthletesCount')"
					:type="'primary'"
					:pill="true"
					@button-click="null" />
			</router-link>
		</div>

		<!-- Disclaimer -->
		<div
			class="border border-black bg-blue-200 rounded-lg w-max max-w-full relative left-1/2 -translate-x-1/2 p-2 text-xl mt-4 text-center">
			<p class="font-semibold text-center">
				{{ t("competitionPontuationDisclaimer.title") }}
			</p>
			<p>
				<span class="font-semibold text-center">1.º </span>
				{{
					t("competitionPontuationDisclaimer.pointForPlace", {
						points: before2024 ? "5.01" : "5.00",
					})
				}}
			</p>
			<p>
				<span class="font-semibold text-center">2.º </span>
				{{
					t("competitionPontuationDisclaimer.pointForPlace", {
						points: before2024 ? "3.01" : "3.00",
					})
				}}
			</p>
			<p>
				<span class="font-semibold text-center">3.º </span>
				{{
					t("competitionPontuationDisclaimer.pointForPlace", {
						points: before2024 ? "1.01" : "1.00",
					})
				}}
			</p>
			<div v-if="!before2024" class="text-lg mt-2 -space-y-1.5">
				<p class="font-medium">
					{{ t("competitionPontuationDisclaimer.extraPointsAfter2024.title") }}
				</p>
				<p>{{ t("competitionPontuationDisclaimer.extraPointsAfter2024.combats") }}</p>
				<p>{{ t("competitionPontuationDisclaimer.extraPointsAfter2024.forms") }}</p>
			</div>
			<br />
			<p class="text-sm">
				<span class="font-semibold">
					{{ t("competitionPontuationDisclaimer.note.title") }}
				</span>
				{{
					t(
						`competitionPontuationDisclaimer.note.${
							before2024 ? "textBefore2024" : "textAfter2024"
						}`
					)
				}}
			</p>
			<p class="text-sm font-normal">
				{{ t("competitionPontuationDisclaimer.clickToSeeDetails") }}
			</p>
		</div>

		<Statistics
			:url="`competitions/results?competition_ids=${props.competition}`"
			:before2024="before2024"
			:immediate="true"
			:competition-id="props.competition"
			:show-penalizations="true" />
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import Statistics from "@/components/athletes/partials/statistics.vue";
import Button from "@/components/partials/button.vue";
import { unauthApi, authApi } from "@/services/api";
import { ref, onMounted } from "vue";
import toast from "@/toast.js";
import store from "@/store";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
});

const loading = ref(true);
const competition = ref(null);
const before2024 = ref(false);

onMounted(async () => {
	try {
		const url = `competitions/no-list/${props.competition}`;
		const { data } =
			store.getters.getUserRole === "ADMIN"
				? await authApi.get(url)
				: await unauthApi.get(url);
		competition.value = data;
		before2024.value = new Date(2024, 0, 1) > new Date(competition.value.competition_start);
		loading.value = false;
	} catch (e) {
		toast.error(t("error.competitionStatisticsNotLoaded"));
	}
});
</script>
