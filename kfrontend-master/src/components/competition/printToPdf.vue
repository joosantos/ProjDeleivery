<template>
	<div v-if="competition != null">
		<div v-if="show" class="inline-flex w-full gap-x-10 ml-4 mt-2">
			<div
				class="border border-black rounded-md max-w-max px-2 py-1 bg-gray-200 hover:bg-gray-300 active:bg-gray-500 select-none cursor-pointer"
				@click="printPdf">
				{{ t("print") }}
			</div>
			<div class="">
				<select
					v-model="area"
					class="border border-black rounded-md w-28 px-2 py-1 bg-gray-200 hover:bg-gray-300 active:bg-gray-500 select-none cursor-pointer">
					<option value="0">{{ t("area.all") }}</option>
					<option value="1">{{ t("area.number", { count: 1 }) }}</option>
					<option value="2">{{ t("area.number", { count: 2 }) }}</option>
					<option value="3">{{ t("area.number", { count: 3 }) }}</option>
					<option value="4">{{ t("area.number", { count: 4 }) }}</option>
					<option value="5">{{ t("area.number", { count: 5 }) }}</option>
					<option value="6">{{ t("area.number", { count: 6 }) }}</option>
					<option value="7">{{ t("area.number", { count: 7 }) }}</option>
					<option value="8">{{ t("area.number", { count: 8 }) }}</option>
					<option value="9">{{ t("area.number", { count: 9 }) }}</option>
					<option value="10">{{ t("area.number", { count: 10 }) }}</option>
				</select>
			</div>
			<div class="">
				<select
					v-model="day"
					class="border border-black rounded-md w-28 px-2 py-1 bg-gray-200 hover:bg-gray-300 active:bg-gray-500 select-none cursor-pointer">
					<option value="0">{{ t("allDay") }}</option>
					<option value="1">{{ t("dayNumber", { number: 1 }) }}</option>
					<option value="2">{{ t("dayNumber", { number: 2 }) }}</option>
					<option value="3">{{ t("dayNumber", { number: 3 }) }}</option>
					<option value="4">{{ t("dayNumber", { number: 4 }) }}</option>
					<option value="5">{{ t("dayNumber", { number: 5 }) }}</option>
					<option value="6">{{ t("dayNumber", { number: 6 }) }}</option>
					<option value="7">{{ t("dayNumber", { number: 7 }) }}</option>
					<option value="8">{{ t("dayNumber", { number: 8 }) }}</option>
					<option value="9">{{ t("dayNumber", { number: 9 }) }}</option>
					<option value="10">{{ t("dayNumber", { number: 10 }) }}</option>
				</select>
			</div>
			<div class="">
				<select
					v-model="time"
					class="border border-black rounded-md w-28 px-2 py-1 bg-gray-200 hover:bg-gray-300 active:bg-gray-500 select-none cursor-pointer">
					<option value="0">{{ t("allDay") }}</option>
					<option value="M">{{ t("morning") }}</option>
					<option value="A">{{ t("afternoon") }}</option>
				</select>
			</div>
		</div>
		<div v-for="tournament of competition.tournaments" :key="tournament.id">
			<div
				v-show="
					(area == 0
						? true
						: tournament.area == null
						? false
						: tournament.area == area) &&
					(day == 0 ? true : tournament.day == null ? false : tournament.day == day) &&
					(time == '0'
						? true
						: time == 'M'
						? tournament.morning
						: time == 'A'
						? !tournament.morning
						: false)
				"
				:id="tournament.id"
				class="relative break-after-page">
				<div
					v-if="
						tournament.category.category_type.name == 'Tournament' &&
						tournament.matches.length > 0
					">
					<Bracket2
						v-if="tournament.matches.length < 2"
						:tournament="tournament"
						:fixed="true" />
					<Bracket3
						v-else-if="tournament.matches.length < 4"
						:tournament="tournament"
						:fixed="true" />
					<Bracket4
						v-else-if="tournament.matches.length < 5"
						:tournament="tournament"
						:fixed="true" />
					<Bracket8
						v-else-if="tournament.matches.length < 9"
						:tournament="tournament"
						:fixed="true" />
					<Bracket16
						v-else-if="tournament.matches.length < 17"
						:tournament="tournament"
						:fixed="true" />
					<Bracket32
						v-else-if="tournament.matches.length < 33"
						:tournament="tournament"
						:fixed="true" />
				</div>
				<div v-else-if="tournament.matches.length > 0">
					<ListTournament :tournament="tournament" :fixed="true" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Bracket2 from "@/components/partials/skeletons/bracket2.vue";
import Bracket3 from "@/components/partials/skeletons/bracket3.vue";
import Bracket4 from "@/components/partials/skeletons/bracket4.vue";
import Bracket8 from "@/components/partials/skeletons/bracket8.vue";
import Bracket16 from "@/components/partials/skeletons/bracket16.vue";
import Bracket32 from "@/components/partials/skeletons/bracket32.vue";
import ListTournament from "@/components/partials/skeletons/listTournament.vue";
import { unauthApi } from "@/services/api";
import { ref } from "vue";
import toast from "@/toast.js";
import store from "@/store";
import { useI18n } from "vue-i18n";

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

let { t } = useI18n();
let area = ref("0");
let time = ref("0");
let day = ref("0");
let show = ref(true);
const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});

let competition = ref(null);

unauthApi
	.get("competitions/" + props.competitionId)
	.then(async (response) => {
		competition.value = response.data;
	})
	.catch(() => {
		toast.error(t("notLoaded"));
	});

async function printPdf() {
	show.value = false;
	setTimeout(() => {
		print();
		show.value = true;
	}, 200);
}
</script>

<i18n>
{
	"en_GB": {
		"print": "Print To PDF",
		"area": {
			"all": "All Areas",
			"number": "Area {count}"
		},
		"dayNumber": "Day {number}",
		"allDay": "All days",
		"afternoon": "Afternoon",
		"morning": "Morning",
		"notLoaded": "Wasn't possible to load the competition",
	},
	"pt_PT": {
		"afternoon": "Tarde",
		"morning": "Manhã",
		"notLoaded": "Não foi possível carregar a competição",
		"dayNumber": "Dia {number}",
		"allDay": "Todos os dias",
	}
}
</i18n>
