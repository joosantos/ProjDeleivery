<script setup>
import GlobalStatisticsForm from "@/components/athletes/partials/globalStatisticsForm.vue";
import Statistics from "@/components/athletes/partials/statistics.vue";
import { ref } from "vue";

const url = ref("competitions/results?");
const before2024 = ref(false);

const updateUrl = async (competitions, year) => {
	let urlBuilder = "competitions/results?";
	for (const competition of competitions) {
		if (competition.selected) urlBuilder += `competition_ids=${competition.id}&`;
	}
	url.value = urlBuilder.slice(0, urlBuilder.length - 1);
	before2024.value = year < 2024;
};
</script>

<template>
	<GlobalStatisticsForm @update-statistics="updateUrl" />
	<Statistics :url="url" :before2024="before2024" :immediate="false" />
</template>
