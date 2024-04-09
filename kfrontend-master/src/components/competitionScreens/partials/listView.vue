<template>
	<!-- Red Side -->
	<div class="col-span-1 bg-red-500 h-[2000px] rounded-3xl">
		<!-- Show poster and podium, language select call athletes, see bracket -->
		<div class="inline-flex mt-5 justify-center w-full px-4 gap-x-12">
			<div>
				<input
					id="showPic"
					v-model="state.showPic"
					name="showPic"
					type="checkbox"
					class="h-10 w-10 rounded-full border-black"
					@change="emit('showPoster', state.showPic)" />
				<label
					for="showPic"
					class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
					{{ t("show.poster") }}
				</label>
			</div>
			<div>
				<Tooltip
					:class="!canToogleShowPodium && 'mt-2'"
					:text="t('tournamentDidNotEnd')"
					:show="!canToogleShowPodium"
					:capitalize="true">
					<input
						id="showPodium"
						v-model="state.showPodium"
						name="showPodium"
						type="checkbox"
						:disabled="!canToogleShowPodium"
						:class="[
							'h-10 w-10 rounded-full border-black',
							!canToogleShowPodium && 'opacity-50 -mt-2',
						]"
						@change="emit('showPodium', state.showPodium)" />
					<label
						for="showPodium"
						class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
						{{ t("show.podium") }}
					</label>
				</Tooltip>
			</div>
			<div>
				<input
					id="morning"
					v-model="state.morning"
					checked
					:value="true"
					name="morning"
					type="radio"
					class="h-10 w-10 rounded-full border-black checked:text-blue-500 active:ring-blue-500 focus:ring-blue-500" />
				<label
					for="morning"
					class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
					{{ t("morning") }}
				</label>
			</div>
			<div>
				<input
					id="afternoon"
					v-model="state.morning"
					:value="false"
					name="morning"
					type="radio"
					class="h-10 w-10 rounded-full border-black checked:text-blue-500 active:ring-blue-500 focus:ring-blue-500" />
				<label
					for="morning"
					class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
					{{ t("afternoon") }}
				</label>
			</div>
			<div>
				<input
					id="competitionDay"
					v-model="state.competitionDay"
					name="competitionDay"
					type="number"
					class="ml-10 h-10 w-20 border-black"
					@change="emit('numberDay', state.competitionDay)" />
				<label
					for="competitionDay"
					class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
					{{ t("competitionDay") }}
				</label>
			</div>
			<MiniTournamentModal v-if="props.tournament != null" :tournament="props.tournament">
				<button
					class="capitalize text-white text-xl font-medium border border-black px-2 py-1 rounded-lg bg-blue-800 cursor-pointer"
					type="button"
					@click="emit('showTournament')">
					{{ t("seeTournament") }}
				</button>
			</MiniTournamentModal>
			<div>
				<button
					type="button"
					class="capitalize text-white text-xl font-medium border border-black px-2 py-1 rounded-lg bg-blue-800 cursor-pointer"
					@click="emit('openCallRequest')">
					{{ t("callAthlete", 2) }}
				</button>
			</div>
			<div>
				<select
					id="locale"
					v-model="locale"
					name="locale"
					class="bg-white appearance-nonecss border-blue-600 border-2 text-black rounded-full">
					<option value="en_GB">
						{{ countriesList.getEmojiFlag("GB") + " English" }}
					</option>
					<option value="pt_PT">
						{{ countriesList.getEmojiFlag("PT") + " Português" }}
					</option>
				</select>
			</div>
		</div>
		<!-- Athlete Info -->
		<div class="max-w-max mx-auto mt-20">
			<p
				class="capitalize text-xl bg-gray-400 px-2 max-w-max border-2 border-b-0 border-black rounded-t-lg">
				{{ t("athlete.name") }}
			</p>
			<input
				v-model="state.athletes.red.name"
				class="text-4xl front-bolf text-center bg-white border-2 border-black w-[800px] rounded-lg rounded-tl-none"
				@change="update" />
			<p
				class="capitalize text-xl mt-6 bg-gray-400 px-2 max-w-max border-2 border-b-0 border-black rounded-t-lg">
				{{ t("athlete.team") }}
			</p>
			<input
				v-model="state.athletes.red.team"
				class="text-4xl uppercase front-bolf br text-center w-full bg-red-300 border-2 border-black rounded-lg rounded-tl-none"
				@change="update" />
		</div>
	</div>

	<!-- Tournament atheltes and points -->
	<div
		v-if="props.tournament?.matches?.length"
		class="absolute right-10 top-1/2 -translate-y-1/2 max-h-[700px] overflow-y-auto w-[400px] bg-red-50 grid rounded-xl divide-y-2 divide-black border-2 border-black">
		<div
			v-for="match in props.tournament.matches"
			:key="match.id"
			:class="[
				'text-xl inline-flex w-full divide-x-2 divide-black tabular-nums',
				match.athlete_red_id == state.athletes.red.id && 'bg-red-300',
			]">
			<p class="py-1 px-1">
				{{ match.number_by_area.toString().padStart(3, "0") }}
			</p>
			<p class="px-2 py-1 line-clamp-1">
				{{ getAthleteNameTeam(match.athlete_red) }}
			</p>
			<p
				v-if="match.points_red_total || match.number_by_area < state.matchNumber"
				class="ml-auto px-2 py-1">
				{{ formatPoints(match.points_red_total) }}
			</p>
		</div>
	</div>

	<!-- Combat Number -->
	<div
		class="absolute left-1/2 -translate-x-1/2 top-[30rem] h-32 w-32 border-2 border-black bg-white rounded-lg">
		<p class="text-3xl text-center line-clamp-1">
			{{ t("matchNumAbbr") }}
		</p>
		<input
			v-model="state.matchNumber"
			class="text-5xl text-center font-semibold w-20 relative left-1/2 -translate-x-1/2"
			@change="emit('match', Number(state.matchNumber))" />
	</div>

	<!-- Match Timer -->
	<div class="absolute left-1/2 -translate-x-1/2 bottom-40">
		<TimerTable
			:modal-open="props.modalOpen"
			:title="t('tableTimer.privateTimer')"
			:save-local="false" />
	</div>

	<!-- Save Match -->
	<div class="absolute bottom-20 left-1/2 -translate-x-1/2 mx-auto">
		<button
			class="capitalize text-3xl font-medium text-center cursor-pointer py-2 border-2 border-black bg-gray-100 w-max px-16 hover:bg-gray-300 rounded-lg"
			@click="emit('saveMatch')">
			{{ t("saveMatchResult") }}
		</button>
	</div>

	<!-- Select Match -->
	<div
		v-show="true"
		class="absolute left-0 translate-x-1/2 bottom-2 border-2 border-black bg-white w-[200px] hover:bg-gray-300 rounded-lg">
		<button
			class="capitalize text-base text-center cursor-pointer w-full rounded-lg"
			@click="emit('selectMatch')">
			{{ t("selectMatch") }}
		</button>
	</div>
</template>

<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import MiniTournamentModal from "@/components/competitionScreens/modals/tournamentMini.vue";
import TimerTable from "@/components/competitionScreens/partials/timerTable.vue";
import { getAthleteName, getAthleteNameTeam, getTeamName } from "@/services/athlete.service";
import { ref, watch, computed } from "vue";
import countriesList from "countries-list";
import { useI18n } from "vue-i18n";

let { t, locale } = useI18n({ useScope: "global" });
const emit = defineEmits([
	"showPoster",
	"showPodium",
	"openCallRequest",
	"dayTime",
	"numberDay",
	"showTournament",
	"match",
	"selectMatch",
	"saveMatch",
]);

let state = ref({
	matchNumber: 1,
	showPic: false,
	showPodium: false,
	morning: true,
	competitionDay: 1,
	athletes: {
		red: {
			name: "",
			team: "",
		},
	},
});
let canToogleShowPodium = computed(
	() => props.tournament.first_place_id !== null || state.value.showPodium
);

const props = defineProps({
	tournament: {
		type: Object,
		required: true,
	},
	matchIndex: {
		type: Number,
		required: true,
	},
	matchNumber: {
		type: Number,
		required: true,
	},
	modalOpen: {
		type: Boolean,
		required: true,
	},
	showPodium: {
		type: Boolean,
		required: true,
	},
});

watch(
	() => props.tournament,
	() => {
		if (!Object.keys(props.tournament).length) return;
		let athleteAux = props.tournament.matches[props.matchIndex].athlete_red;
		state.value.athletes.red.name = getAthleteName(athleteAux);
		state.value.athletes.red.team = getTeamName(athleteAux);
		state.value.athletes.red.id = athleteAux.id;
		state.value.morning = props.tournament.morning;
		state.value.competitionDay = props.tournament.day;
		update();
	},
	{ deep: true, immediate: true }
);

watch(
	() => props.matchNumber,
	() => {
		state.value.matchNumber = props.matchNumber;
		update();
	},
	{ immediate: true }
);

watch(
	() => props.showPodium,
	() => {
		state.value.showPodium = props.showPodium;
		update();
	},
	{ immediate: true }
);

watch(
	() => state.value.morning,
	() => {
		emit("dayTime", state.value.morning);
	}
);

watch(
	() => locale.value,
	() => {
		localStorage.setItem("local-language", locale.value);
	}
);

function update() {
	localStorage.setItem("tournamentAthletesInfo", JSON.stringify(state.value));
}

function formatPoints(points) {
	if (!points) return "00.00";

	return points.toFixed(2);
}
</script>
