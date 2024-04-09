<template>
	<Loading v-if="loading" />
	<div
		v-else
		class="my-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-x-4 gap-y-4">
		<div
			v-for="i in 12"
			v-show="(matches[i] || []).length !== 0"
			:key="i"
			class="col-span-1 bg-blue-50 rounded-xl pt-2 pb-4">
			<p class="text-center text-xl font-medium">
				{{ t("area", { area: i }) }}
			</p>
			<div class="space-y-2 mx-4">
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
							<div class="inline-flex justify-between w-full gap-x-4 font-medium">
								<p>{{ t("match", { number: match.number_by_area }) }}</p>
								<p>{{ t(`callType.${match.call_type}`) }}</p>
							</div>
							<p
								v-if="getAthleteNameTeam(match.athlete_red) != ''"
								class="bg-red-400 px-2 py-0.5 rounded-full whitespace-pre-line">
								{{ getAthleteNameTeam(match.athlete_red).replaceAll(", ", "\n") }}
							</p>
							<p
								v-if="getAthleteNameTeam(match.athlete_blue) != ''"
								class="bg-blue-400 px-2 py-0.5 rounded-full whitespace-pre-line">
								{{ getAthleteNameTeam(match.athlete_blue).replaceAll(", ", "\n") }}
							</p>
						</div>
					</router-link>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { getAthleteNameTeam as getName } from "@/services/athlete.service.js";
import { ref } from "vue";
import { unauthApi } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

store.commit("setShowNavBar", false);

let { t } = useI18n();
let loading = ref(true);
let promiseRequest = ref(null);
let timer = ref(0);
let promiseTimer = ref(null);
let matches = ref(null);

const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});
getMatches();
function getMatches() {
	unauthApi
		.get(`competitions/${props.competitionId}/show-by-area`)
		.then((response) => {
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
		.catch((error) => {
			console.error("Error Getting Matches", error);
			toast.error(t("matchesError"));
			loading.value = false;
		});
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
</script>

<i18n>
{
  	"en_GB": {
		"matchesError": "Error getting matches, please try again later.",
		"area": "Area {area}",
		"match": "Match {number}",
		"callType": {
			"c": "Called",
			"p": "Preparing",
			"s": "Called Twice",
			"l": "Last Call",
			"o": "Other"
		},
	},
	"pt_PT": {
		"matchesError": "Erro a receber provas, por favor tente de novo mais tarde.",
		"area": "Área {area}",
		"match": "Disputa {number}",
		"callType": {
			"c": "Chamado",
			"p": "A Preparar",
			"s": "Chamado duas vezes",
			"l": "Última Chamada",
			"o": "Outro"
		},
	}
}
</i18n>
