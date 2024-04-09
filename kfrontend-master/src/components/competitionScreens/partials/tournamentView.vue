<template>
	<div class="w-full grid grid-cols-2 gap-x-8">
		<!-- Red Side -->
		<div class="col-span-1 bg-red-500 rounded-t-3xl h-[2000px]">
			<!-- Hide points, fouls, poster and language select -->
			<div class="inline-flex mt-5 justify-between w-full px-4">
				<div>
					<input
						id="hidePoints"
						v-model="state.hidePoints"
						name="hidePoints"
						type="checkbox"
						class="h-10 w-10 rounded-full border-black"
						@change="emit('hidePoints', state.hidePoints)" />
					<label
						for="hidePoints"
						class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
						{{ t("hide.points") }}
					</label>
				</div>
				<div>
					<input
						id="hideFouls"
						v-model="state.hideFouls"
						name="hideFouls"
						type="checkbox"
						class="h-10 w-10 rounded-full border-black"
						@change="emit('hideFouls', state.hideFouls)" />
					<label
						for="hideFouls"
						class="capitalize text-white text-xl font-medium ml-1 relative top-0.5">
						{{ t("hide.fouls") }}
					</label>
				</div>
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
					<button
						type="button"
						class="capitalize text-white text-xl font-medium ml-5 border border-black px-2 py-1 rounded-lg bg-blue-800 cursor-pointer"
						@click="emit('openCallRequest')">
						{{ t("callAthlete", 2) }}
					</button>
				</div>
				<div class="ml-4">
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
			<div class="w-max max-w-[800px] mx-auto mt-20">
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
					class="text-4xl front-bolf br text-center w-full bg-red-300 border-2 border-black rounded-lg rounded-tl-none"
					@change="update" />

				<div v-if="!state.hideFouls" class="w-min mt-4">
					<p class="capitalize text-center text-4xl font-bold text-white">
						{{ t("fouls") }}
					</p>
					<div class="inline-flex">
						<div class="border border-black bg-white w-28 h-28 relative rounded-l-lg">
							<p
								class="capitalize m-auto w-min text-red-500 font-bold text-8xl top-1/2 -translate-y-1/2 relative">
								{{
									state.athletes.red.fouls == 1
										? t("foulsWarning")
										: state.athletes.red.fouls == 0
										? state.athletes.red.fouls
										: state.athletes.red.fouls - 1
								}}
							</p>
						</div>
						<div>
							<Tooltip :text="t('tooltips.red.fouls.add')">
								<div
									class="bg-white border-black border border-l-0 cursor-pointer rounded-r-lg hover:bg-gray-300"
									@click="
										++state.athletes.red.fouls;
										update();
									">
									<PlusIcon class="h-10 w-10" />
								</div>
							</Tooltip>
							<Tooltip :text="t('tooltips.red.fouls.remove')">
								<div
									class="bg-white border-black border border-l-0 mt-7 cursor-pointer rounded-r-lg hover:bg-gray-300"
									@click="
										--state.athletes.red.fouls;
										update();
									">
									<MinusIcon class="w-10 h-10" />
								</div>
							</Tooltip>
						</div>
					</div>
				</div>
				<div
					v-if="!state.hidePoints"
					class="text-4xl mt-4 w-min font-bold text-white mx-auto">
					<p class="capitalize text-center">{{ t("points") }}</p>
					<div class="inline-flex">
						<div class="border border-black bg-white w-40 h-40 relative rounded-l-lg">
							<p
								class="m-auto w-min text-black font-bold text-9xl top-1/2 -translate-y-1/2 relative">
								{{ state.athletes.red.points }}
							</p>
						</div>
						<div>
							<Tooltip :text="t('tooltips.red.points.add')">
								<div
									class="bg-white border-black border border-l-0 cursor-pointer text-black rounded-r-lg hover:bg-gray-300"
									@click="
										++state.athletes.red.points;
										update();
									">
									<PlusIcon class="h-10 w-10" />
								</div>
							</Tooltip>
							<Tooltip :text="t('tooltips.red.points.remove')">
								<div
									class="bg-white border-black border border-l-0 mt-[4.75rem] cursor-pointer text-black rounded-r-lg hover:bg-gray-300"
									@click="
										--state.athletes.red.points;
										update();
									">
									<MinusIcon class="w-10 h-10" />
								</div>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Blue Side -->
		<div class="col-span-1 bg-blue-500 rounded-t-3xl">
			<!-- Chose competition time and day, See tournament -->
			<div class="inline-flex mt-5 ml-10">
				<div>
					<input
						id="morning"
						v-model="state.morning"
						checked
						:value="true"
						name="morning"
						type="radio"
						class="ml-10 h-10 w-10 rounded-full border-black checked:text-red-500 active:ring-red-500 focus:ring-red-500" />
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
						class="ml-10 h-10 w-10 rounded-full border-black checked:text-red-500 active:ring-red-500 focus:ring-red-500" />
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
						class="capitalize text-white text-xl font-medium ml-5 border border-black px-2 py-1 rounded-lg bg-blue-800 cursor-pointer"
						type="button"
						@click="emit('showTournament')">
						{{ t("seeTournament") }}
					</button>
				</MiniTournamentModal>
			</div>

			<!-- Athlete Info -->
			<div class="w-max max-w-[800px] mx-auto mt-20">
				<p
					class="capitalize text-xl bg-gray-400 px-2 max-w-max border-2 border-b-0 border-black rounded-t-lg">
					{{ t("athlete.name") }}
				</p>
				<input
					v-model="state.athletes.blue.name"
					class="text-4xl front-bolf text-center bg-white border-2 border-black w-[800px] rounded-lg rounded-tl-none"
					@change="update" />
				<p
					class="capitalize text-xl mt-6 bg-gray-400 px-2 max-w-max border-2 border-b-0 border-black rounded-t-lg">
					{{ t("athlete.team") }}
				</p>
				<input
					v-model="state.athletes.blue.team"
					class="text-4xl front-bolf br text-center w-full bg-blue-300 border-2 border-black rounded-lg rounded-tl-none"
					@change="update" />

				<div v-if="!state.hideFouls" class="w-min mt-4 ml-auto">
					<p class="capitalize text-center text-4xl font-bold text-white">
						{{ t("fouls") }}
					</p>
					<div class="inline-flex">
						<div>
							<Tooltip :text="t('tooltips.blue.fouls.add')">
								<div
									class="bg-white border-black border border-l-0 cursor-pointer rounded-l-lg hover:bg-gray-300"
									@click="
										++state.athletes.blue.fouls;
										update();
									">
									<PlusIcon class="h-10 w-10" />
								</div>
							</Tooltip>
							<Tooltip :text="t('tooltips.blue.fouls.remove')">
								<div
									class="bg-white border-black border border-l-0 mt-7 cursor-pointer rounded-l-lg hover:bg-gray-300"
									@click="
										--state.athletes.blue.fouls;
										update();
									">
									<MinusIcon class="w-10 h-10" />
								</div>
							</Tooltip>
						</div>
						<div class="border border-black bg-white w-28 h-28 relative rounded-r-lg">
							<p
								class="capitalize m-auto w-min text-red-500 font-bold text-8xl top-1/2 -translate-y-1/2 relative">
								{{
									state.athletes.blue.fouls == 1
										? t("foulsWarning")
										: state.athletes.blue.fouls == 0
										? state.athletes.blue.fouls
										: state.athletes.blue.fouls - 1
								}}
							</p>
						</div>
					</div>
				</div>
				<div
					v-if="!state.hidePoints"
					:class="[
						'text-4xl mt-4 w-min font-bold text-white mx-auto',
						state.hideFouls && 'mr-auto',
					]">
					<p class="capitalize text-center">{{ t("points") }}</p>
					<div class="inline-flex">
						<div>
							<Tooltip :text="t('tooltips.blue.points.add')">
								<div
									class="bg-white border-black border border-l-0 cursor-pointer text-black rounded-l-lg hover:bg-gray-300"
									@click="
										++state.athletes.blue.points;
										update();
									">
									<PlusIcon class="h-10 w-10" />
								</div>
							</Tooltip>
							<Tooltip :text="t('tooltips.blue.points.remove')">
								<div
									class="bg-white border-black border border-l-0 mt-[4.75rem] cursor-pointer text-black rounded-l-lg hover:bg-gray-300"
									@click="
										--state.athletes.blue.points;
										update();
									">
									<MinusIcon class="w-10 h-10" />
								</div>
							</Tooltip>
						</div>
						<div class="border border-black bg-white w-40 h-40 relative rounded-r-lg">
							<p
								class="m-auto w-min text-black font-bold text-9xl top-1/2 -translate-y-1/2 relative">
								{{ state.athletes.blue.points }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Match Number -->
		<div
			class="absolute left-1/2 -translate-x-1/2 top-40 h-32 w-32 border-2 border-black bg-white rounded-lg">
			<p class="text-3xl text-center line-clamp-1">{{ t("matchNumAbbr") }}</p>
			<input
				v-model="state.matchNumber"
				class="text-5xl text-center font-semibold w-20 relative left-1/2 -translate-x-1/2"
				@change="emit('match', Number(state.matchNumber))" />
		</div>

		<!-- Only Table Timer -->
		<div
			:class="[
				'absolute left-1/2 -translate-x-1/2',
				hideSecondaryTimer ? 'bottom-[34rem]' : 'bottom-[26rem]',
			]">
			<TimerTable
				v-show="!hideSecondaryTimer"
				:modal-open="props.modalOpen"
				:secondary="true"
				:title="t('tableTimer.privateTimer')"
				:save-local="false"
				@hide="hideSecondaryTimer = true" />
			<div
				v-show="hideSecondaryTimer"
				class="bg-blue-100 border-2 border-black rounded-lg cursor-pointer"
				@click="hideSecondaryTimer = false">
				<p class="px-4 py-2 text-lg font-medium capitalize">
					{{ t("tableTimer.showPrivateTimer") }}
				</p>
			</div>
		</div>

		<!-- Match Timer, save points and match buttons -->
		<div class="absolute bottom-20 left-1/2 -translate-x-1/2 space-y-2">
			<!-- Match Timer -->
			<TimerTable :modal-open="props.modalOpen" />

			<!-- Save Points -->
			<div
				class="mx-auto py-2 border-2 border-black w-max px-8 hover:bg-gray-400 rounded-lg bg-gray-300">
				<button
					class="capitalize text-xl font-medium text-center cursor-pointer w-full rounded-lg"
					@click="emit('savePoints')">
					{{ t("savePoints") }}
				</button>
			</div>

			<!-- Save Match -->
			<div class="mx-auto max-w-max">
				<button
					class="capitalize py-2 border-2 border-black bg-gray-100 px-16 hover:bg-gray-300 rounded-lg text-3xl font-medium text-center cursor-pointer w-max"
					@click="emit('saveMatch')">
					{{ t("saveMatchResult") }}
				</button>
			</div>
		</div>

		<!-- Seect Match -->
		<div
			class="absolute bottom-2 left-8 border-2 border-black bg-white w-[200px] hover:bg-gray-300 rounded-lg">
			<button
				class="capitalize text-base text-center cursor-pointer w-full rounded-lg"
				@click="emit('selectMatch')">
				{{ t("selectMatch") }}
			</button>
		</div>

		<!-- Declare Winner Red Side -->
		<div
			class="absolute bottom-10 left-10 border-2 border-black bg-yellow-300 p-2 text-xl cursor-pointer rounded-lg hover:bg-yellow-500"
			@click="emit('winner', 1)">
			<Tooltip :text="t('tooltips.red.declare')">
				<p>
					{{ t("declareWinner") }}
				</p>
			</Tooltip>
		</div>

		<!-- Declare Winner Blue Side -->
		<div
			class="absolute bottom-10 right-10 border-2 border-black bg-yellow-300 p-2 text-xl cursor-pointer rounded-lg hover:bg-yellow-500"
			@click="emit('winner', 2)">
			<Tooltip :text="t('tooltips.blue.declare')">
				<p>
					{{ t("declareWinner") }}
				</p>
			</Tooltip>
		</div>
	</div>
</template>

<script setup>
import MiniTournamentModal from "@/components/competitionScreens/modals/tournamentMini.vue";
import Tooltip from "@/components/partials/templates/tooltip.vue";
import TimerTable from "@/components/competitionScreens/partials/timerTable.vue";
import { getAthleteName, getTeamName } from "@/services/athlete.service";
import { ref, watch } from "vue";
import { PlusIcon, MinusIcon } from "@heroicons/vue/24/solid";
import countriesList from "countries-list";
import { useI18n } from "vue-i18n";

let { t, locale } = useI18n({ useScope: "global" });
const emit = defineEmits([
	"hidePoints",
	"hideFouls",
	"showPoster",
	"openCallRequest",
	"dayTime",
	"numberDay",
	"showTournament",
	"match",
	"selectMatch",
	"saveMatch",
	"savePoints",
	"winner",
]);
let hideSecondaryTimer = ref(true);
let state = ref({
	hidePoints: false,
	hideFouls: false,
	matchNumber: 1,
	showPic: false,
	morning: true,
	competitionDay: 1,
	athletes: {
		red: {
			name: "",
			team: "",
			fouls: 0,
			points: 0,
		},
		blue: {
			name: "",
			team: "",
			fouls: 0,
			points: 0,
		},
	},
});

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
});

watch(
	() => props.tournament,
	() => {
		if (!Object.keys(props.tournament).length) return;

		state.value.athletes.red.name = getAthleteName(
			props.tournament.matches[props.matchIndex].athlete_red
		);
		state.value.athletes.red.team = getTeamName(
			props.tournament.matches[props.matchIndex].athlete_red
		);
		state.value.athletes.red.fouls = 0;
		state.value.athletes.red.points = 0;
		state.value.athletes.blue.name = getAthleteName(
			props.tournament.matches[props.matchIndex].athlete_blue
		);
		state.value.athletes.blue.team = getTeamName(
			props.tournament.matches[props.matchIndex].athlete_blue
		);
		state.value.athletes.blue.fouls = 0;
		state.value.athletes.blue.points = 0;
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

window.addEventListener("keypress", function (event) {
	if (event.target.tagName == "INPUT" || event.target.tagName == "TEXTAREA" || props.modalOpen) {
		return;
	}

	switch (event.code) {
		case "NumpadDivide":
			event.preventDefault();
			state.value.athleteRed.fouls += 1;
			update();
			break;
		case "Numpad8":
			event.preventDefault();
			state.value.athleteRed.fouls -= 1;
			update();
			break;
		case "Numpad5":
			event.preventDefault();
			state.value.athleteRed.points += 1;
			update();
			break;
		case "Numpad2":
			event.preventDefault();
			state.value.athleteRed.points -= 1;
			update();
			break;
		case "NumpadMultiply":
			event.preventDefault();
			state.value.athleteBlue.fouls += 1;
			update();
			break;
		case "Numpad9":
			event.preventDefault();
			state.value.athleteBlue.fouls -= 1;
			update();
			break;
		case "Numpad6":
			event.preventDefault();
			state.value.athleteBlue.points += 1;
			update();
			break;
		case "Numpad3":
			event.preventDefault();
			state.value.athleteBlue.points -= 1;
			update();
			break;
		case "Numpad0":
			event.preventDefault();
			if (state.value.winner != 0) {
				state.value.winner = 0;
				update();
				return;
			}
			state.value.winner = 1;
			update();
			break;
		case "NumpadEnter":
			event.preventDefault();
			if (state.value.winner != 0) {
				state.value.winner = 0;
				update();
				return;
			}
			state.value.winner = 2;
			update();
			break;
	}
});
</script>
