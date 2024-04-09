<template>
	<div>
		<Loading v-if="loading" />
		<div v-else>
			<div class="inline-flex gap-x-8">
				<CustomInput
					class="w-40"
					:type="'text'"
					:mask="'###'"
					:name="'day'"
					:label="t('competitionDay')"
					:option-selected="day.toString()"
					:error="''"
					@value-changed="(option) => (day = option)" />
				<Button
					class="max-w-max"
					:loading="showSpinningWheel"
					:message="t('refreshMatches')"
					type="primary"
					@button-click="refreshMatches" />
			</div>
			<div
				class="my-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-x-4 gap-y-4">
				<div v-for="i in 12" :key="i" class="col-span-1 bg-blue-50 rounded-xl pt-2 pb-4">
					<p class="text-center text-xl font-medium">
						{{ t("areaNumber", { number: i }) }}
					</p>
					<div class="space-y-2 mx-4">
						<div v-if="numbers != null && numbers[i] != null">
							<p class="font-semibold text-xl">{{ t("matches") }}</p>
							<CustomInput
								class="w-32"
								:type="'text'"
								:mask="'###'"
								:name="'name' + i"
								:label="t('timePerMatch')"
								:option-selected="timePerMatch[i].toString()"
								:error="''"
								@value-changed="
									(option) => {
										timePerMatch[i] = option;
										updateTimeLeft();
									}
								" />
							<div>
								<table class="min-w-full text-left text-sm font-light">
									<thead class="border-b font-medium dark:border-neutral-500">
										<tr>
											<th scope="col" class="px-6 py-4">
												{{ t("timeOfTheDay") }}
											</th>
											<th scope="col" class="px-6 py-4">
												{{ t("actualMatch") }}
											</th>
											<th scope="col" class="px-6 py-4">
												{{ t("lastMatch") }}
											</th>
											<th scope="col" class="px-6 py-4">
												{{ t("timeLeft") }}
											</th>
											<th scope="col" class="px-6 py-4">
												{{ t("endHours") }}
											</th>
										</tr>
									</thead>
									<tbody>
										<tr v-if="numbers[i][true] != null" class="border-b">
											<td class="whitespace-nowrap px-6 py-4 font-medium">
												{{ t("morning") }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ numbers[i][true]["min"] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ numbers[i][true]["max"] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ timeLeft[i][true] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ endTime[i][true] }}
											</td>
										</tr>
										<tr v-if="numbers[i][false] != null" class="border-b">
											<td class="whitespace-nowrap px-6 py-4 font-medium">
												{{ t("afternoon") }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ numbers[i][false]["min"] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ numbers[i][false]["max"] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ timeLeft[i][false] }}
											</td>
											<td class="whitespace-nowrap px-6 py-4">
												{{ endTime[i][false] }}
											</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
						<div
							v-for="match in matches[i] || []"
							:key="match.id"
							:class="[
								'rounded-xl',
								match.call_type == 'p'
									? 'bg-blue-200'
									: match.call_type == 'c'
									? 'bg-green-200'
									: match.call_type == 'o'
									? 'bg-blue-200'
									: 'bg-yellow-200',
							]">
							<router-link
								target="_blank"
								:to="{
									name: 'Show Tournament',
									params: { tournament: match.tournament_id },
								}">
								<div
									class="mx-4 space-y-2 text-center pt-1 pb-2 select-none cursor-pointer">
									<div
										class="inline-flex justify-between w-full gap-x-4 font-medium">
										<p>{{ t("matchNum", { number: match.number_by_area }) }}</p>
										<p>{{ t(`microphone.callType.${match.call_type}`) }}</p>
									</div>
									<p
										v-if="getAthleteNameTeam(match.athlete_red) != ''"
										class="bg-red-400 px-2 py-0.5 rounded-full whitespace-pre-line">
										{{
											getAthleteNameTeam(match.athlete_red).replaceAll(
												", ",
												"\n"
											)
										}}
									</p>
									<p
										v-if="getAthleteNameTeam(match.athlete_blue) != ''"
										class="bg-blue-400 px-2 py-0.5 rounded-full whitespace-pre-line">
										{{
											getAthleteNameTeam(match.athlete_blue).replaceAll(
												", ",
												"\n"
											)
										}}
									</p>
								</div>
							</router-link>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { getAthleteNameTeam as getName } from "@/services/athlete.service.js";
import { ref } from "vue";
import { unauthApi, authApi } from "@/services/api";
import Button from "@/components/partials/button.vue";
import store from "@/store";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

store.commit("setShowNavBar", false);
let timePerMatch = ref(JSON.parse(localStorage.getItem("matchTimeByArea")));
if (timePerMatch.value == null) {
	timePerMatch.value = {
		1: 10,
		2: 10,
		3: 10,
		4: 10,
		5: 10,
		6: 10,
		7: 10,
		8: 10,
		9: 10,
		10: 10,
		11: 10,
		12: 10,
	};
}
let timeLeft = ref({
	1: { true: "00:00", false: "00:00" },
	2: { true: "00:00", false: "00:00" },
	3: { true: "00:00", false: "00:00" },
	4: { true: "00:00", false: "00:00" },
	5: { true: "00:00", false: "00:00" },
	6: { true: "00:00", false: "00:00" },
	7: { true: "00:00", false: "00:00" },
	8: { true: "00:00", false: "00:00" },
	9: { true: "00:00", false: "00:00" },
	10: { true: "00:00", false: "00:00" },
	11: { true: "00:00", false: "00:00" },
	12: { true: "00:00", false: "00:00" },
});
let endTime = ref({
	1: { true: "00:00", false: "00:00" },
	2: { true: "00:00", false: "00:00" },
	3: { true: "00:00", false: "00:00" },
	4: { true: "00:00", false: "00:00" },
	5: { true: "00:00", false: "00:00" },
	6: { true: "00:00", false: "00:00" },
	7: { true: "00:00", false: "00:00" },
	8: { true: "00:00", false: "00:00" },
	9: { true: "00:00", false: "00:00" },
	10: { true: "00:00", false: "00:00" },
	11: { true: "00:00", false: "00:00" },
	12: { true: "00:00", false: "00:00" },
});

function updateTimeLeft() {
	localStorage.setItem("matchTimeByArea", JSON.stringify(timePerMatch));
	localStorage.setItem("dayCompetition", JSON.stringify(day.value));
	for (let i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) {
		if (numbers.value[i] == null) continue;
		if (numbers.value[i][true] != null) {
			timeLeft.value[i][true] = getTimeLeft(
				Number(timePerMatch.value[i]),
				numbers.value[i][true]["min"] || 0,
				numbers.value[i][true]["max"] || 0
			);
			endTime.value[i][true] = getEndingTime(
				Number(timePerMatch.value[i]),
				numbers.value[i][true]["min"] || 0,
				numbers.value[i][true]["max"] || 0
			);
		}
		if (numbers.value[i][false] != null) {
			timeLeft.value[i][false] = getTimeLeft(
				Number(timePerMatch.value[i]),
				numbers.value[i][false]["min"] || 0,
				numbers.value[i][false]["max"] || 0
			);
			endTime.value[i][false] = getEndingTime(
				Number(timePerMatch.value[i]),
				numbers.value[i][false]["min"] || 0,
				numbers.value[i][false]["max"] || 0
			);
		}
	}
}

let { t } = useI18n({ useScope: "global" });
let loading = ref(true);
let promiseRequest = ref(null);
let timer = ref(0);
let promiseTimer = ref(null);

let day = ref(ref(JSON.parse(localStorage.getItem("dayCompetition")) || 1));
let matches = ref(null);
let numbers = ref(null);

const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});
getMatches();
function getMatches() {
	let promises = [];
	promises.push(
		authApi
			.get(`competitions/${props.competitionId}/get-time-left/day/${day.value}`)
			.then((response) => {
				numbers.value = response.data;
				updateTimeLeft();
			})
	);
	promises.push(
		unauthApi.get(`competitions/${props.competitionId}/show-by-area`).then((response) => {
			matches.value = {};
			for (let match of response.data) {
				let area = match.area_to_call;
				if (!(area in matches.value)) matches.value[area] = [];
				matches.value[area].push(match);
			}
			for (let index of Object.keys(matches.value)) {
				matches.value[index].sort((a, b) => {
					if (a.call_type == "p") {
						return 1;
					}
					if (b.call_type == "p") {
						return -1;
					}
					return 0;
				});
			}
			promiseRequest.value = setTimeout(makeCallNow, 30000);
			timer.value = 31;
			loading.value = false;
		})
	);

	Promise.all(promises).catch((error) => {
		console.error("Error Getting Matches", error);
		toast.error(t("genericError"));
		loading.value = false;
	});
}

function refreshMatches() {
	matches.value = [];
	makeCallNow();
}

function makeCallNow() {
	clearInterval(promiseRequest.value);
	clearInterval(promiseTimer.value);
	getMatches();
}

function getAthleteNameTeam(athlete) {
	let name = getName(athlete);
	if (!name) return "";
	return name;
}

setTimeout(() => {
	location.reload();
}, 300000);

function getTimeLeft(time, min, max) {
	let total = Number(time) * (max - min + 1);
	let hours = Math.floor(total / 60).toString();
	let minutes = (total % 60).toString();
	let pad = "00";
	let now = new Date();
	now.setHours(now.getHours() + hours);
	now.setMinutes(now.getMinutes() + minutes);

	return `${pad.substring(0, pad.length - hours.length) + hours}:${
		pad.substring(0, pad.length - minutes.length) + minutes
	}`;
}
function getEndingTime(time, min, max) {
	let total = Number(time) * (max - min + 1);
	let hours = Math.floor(total / 60);
	let minutes = total % 60;
	let now = new Date();
	let pad = "00";

	now.setHours(now.getHours() + hours);
	now.setMinutes(now.getMinutes() + minutes);
	hours = now.getHours().toString();
	minutes = now.getMinutes().toString();

	return `${pad.substring(0, pad.length - hours.length) + hours}:${
		pad.substring(0, pad.length - minutes.length) + minutes
	}`;
}
</script>
