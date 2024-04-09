<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="w-full">
		<table class="mx-auto mt-10 text-center text-2xl">
			<p class="text-2xl font-semibold">
				{{ t("athlete") }}
			</p>
			<p class="text-4xl font-bold">
				{{ athleteName }}
			</p>
			<p class="text-sm font-normal">
				{{ t("note") }}
			</p>
			<p class="">
				{{
					"Tournaments Participated: " +
					(participated.length + first.length + second.length + third.length)
				}}
			</p>
			<table :class="['w-full mt-10', first.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-[#FFD700] border border-black border-b-0',
						first.length == 0 && 'opacity-50',
					]">
					{{
						t("first")
					}}
				</caption>
				<tr
					v-if="first.length == 0"
					class="bg-yellow-100 border border-black divide-y divide-black">
					<div>{{ t("none") }}</div>
				</tr>
				<tr
					v-for="tourn in first"
					:key="tourn.name"
					class="bg-yellow-100 border border-black divide-y divide-black">
					<router-link
						:to="{
							name: 'Show Tournament',
							params: { tournament: tourn.id },
						}"
						target="_blank">
						{{ tourn.name }}
					</router-link>
				</tr>
			</table>
			<table :class="['w-full mt-10', second.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-[#BFBFBF] border border-black border-b-0',
						second.length == 0 && 'opacity-50',
					]">
					{{
						t("second")
					}}
				</caption>
				<tr
					v-if="second.length == 0"
					class="bg-gray-100 border border-black divide-y divide-black">
					<div>{{ t("none") }}</div>
				</tr>
				<tr
					v-for="tourn in second"
					:key="tourn.name"
					class="bg-gray-100 border border-black divide-y divide-black">
					<router-link
						:to="{
							name: 'Show Tournament',
							params: { tournament: tourn.id },
						}"
						target="_blank">
						{{ tourn.name }}
					</router-link>
				</tr>
			</table>
			<table :class="['w-full mt-10', third.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-[#CD7F32] border border-black border-b-0',
						third.length == 0 && 'opacity-50',
					]">
					{{
						t("third")
					}}
				</caption>
				<tr
					v-if="third.length == 0"
					class="bg-orange-100 border border-black divide-y divide-black">
					<div>{{ t("none") }}</div>
				</tr>
				<tr
					v-for="tourn in third"
					:key="tourn.name"
					class="bg-orange-100 border border-black divide-y divide-black">
					<router-link
						:to="{
							name: 'Show Tournament',
							params: { tournament: tourn.id },
						}"
						target="_blank">
						{{ tourn.name }}
					</router-link>
				</tr>
			</table>
			<table :class="['w-full mt-10', participated.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-blue-400 border border-black border-b-0',
						participated.length == 0 && 'opacity-50',
					]">
					{{
						t("others")
					}}
				</caption>
				<tr
					v-if="participated.length == 0"
					class="bg-blue-100 border border-black divide-y divide-black">
					<div>{{ t("none") }}</div>
				</tr>
				<tr
					v-for="tourn in participated"
					:key="tourn.name"
					class="bg-blue-100 border border-black divide-y divide-black">
					<router-link
						:to="{
							name: 'Show Tournament',
							params: { tournament: tourn.id },
						}"
						target="_blank">
						{{ tourn.name }}
					</router-link>
				</tr>
			</table>
		</table>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { unauthApi } from "@/services/api";
import { ref } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";
import { getAthleteNameTeam } from "@/services/athlete.service.js";

let { t } = useI18n();

const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
	// ID of the athlete
	athleteId: {
		type: String,
		required: true,
	},
});

let loading = ref(true);

let tournaments = ref(null);
let first = ref([]);
let second = ref([]);
let third = ref([]);
let other = ref([]);
let participated = ref([]);
let athleteName = ref("");

unauthApi
	.get(`competitions/${props.competition}/athletes/${props.athleteId}`)
	.then((response) => {
		for (let t of response.data) {
			console.log(getName(t));
		}
		console.log(response.data);
		tournaments.value = response.data;
		let aux = {};
		tournamentsLoop: for (let tournament of tournaments.value) {
			if (tournament.first_place_id != null) {
				for (let athlete_group of tournament.first_place.athletes_group) {
					if (athlete_group.athlete_id == props.athleteId) {
						aux = {
							name: getName(tournament),
							id: tournament.id,
							category: tournament.category.name,
						};
						first.value.push(aux);
						if (athleteName.value == "") {
							athleteName.value = getAthleteNameTeam(tournament.first_place);
						}
						continue tournamentsLoop;
					}
				}
			}
			if (tournament.second_place_id != null) {
				for (let athlete_group of tournament.second_place.athletes_group) {
					if (athlete_group.athlete_id == props.athleteId) {
						aux = {
							name: getName(tournament),
							id: tournament.id,
							category: tournament.category.name,
						};
						second.value.push(aux);
						if (athleteName.value == "") {
							athleteName.value = getAthleteNameTeam(tournament.second_place);
						}
						continue tournamentsLoop;
					}
				}
			}
			if (tournament.third_place_id != null) {
				for (let athlete_group of tournament.third_place.athletes_group) {
					if (athlete_group.athlete_id == props.athleteId) {
						aux = {
							name: getName(tournament),
							id: tournament.id,
							category: tournament.category.name,
						};
						third.value.push(aux);
						if (athleteName.value == "") {
							athleteName.value = getAthleteNameTeam(tournament.third_place);
						}
						continue tournamentsLoop;
					}
				}
			}
			for (let match of tournament.matches) {
				if (match.athlete_red_id != null) {
					for (let athlete_group of match.athlete_red.athletes_group) {
						if (athlete_group.athlete_id == props.athleteId) {
							aux = {
								name: getName(tournament),
								id: tournament.id,
								category: tournament.category.name,
							};
							participated.value.push(aux);
							if (athleteName.value == "") {
								athleteName.value = getAthleteNameTeam(match.athlete_red);
							}
							continue tournamentsLoop;
						}
					}
				}
				if (match.athlete_blue_id != null) {
					for (let athlete_group of match.athlete_blue.athletes_group) {
						if (athlete_group.athlete_id == props.athleteId) {
							aux = {
								name: getName(tournament),
								id: tournament.id,
								category: tournament.category.name,
							};
							participated.value.push(aux);
							if (athleteName.value == "") {
								athleteName.value = getAthleteNameTeam(match.athlete_blue);
							}
							continue tournamentsLoop;
						}
					}
				}
			}
		}
		loading.value = false;
	})
	.catch((e) => {
		console.log(e);
		toast.error(t("notLoaded"));
	});

function getName(tourn) {
	let name =
		tourn.category.name +
		(tourn.is_male == null ? "" : " | " + (tourn.is_male ? "Masc." : "Fem."));

	if (tourn.age_min == null && tourn.age_min == null) {
		name += "";
	} else {
		if (tourn.age_min == null) {
			name += " | -" + tourn.age_max + " Years";
		} else {
			if (tourn.age_max == null) {
				name += " | +" + tourn.age_min + " Years";
			} else {
				name += " | " + tourn.age_min + "/" + tourn.age_max + " Years";
			}
		}
	}

	if (tourn.belt == null) {
		if (tourn.weight_min == null && tourn.weight_max == null) {
			name += "";
		} else {
			if (tourn.weight_min == null) {
				name += " | -" + tourn.weight_max + " Kg";
			} else {
				if (tourn.weight_max == null) {
					name += " | +" + tourn.weight_min + " Kg";
				} else {
					name += " | " + tourn.weight_min + "/" + tourn.weight_max + " Kg.";
				}
			}
		}
	} else {
		tourn.name += " | " + tourn.belt;
	}

	return name;
}
</script>

<i18n>
{
  "en_GB": {
	  "first": "First Place",
	  "second": "Second Place",
	  "third": "Third Place",
	  "others": "Others Participated",
	  "athlete": "Results for the Athlete",
	  "none": "None",
	  "note": "To see the bracket, click on the tournament name",
	  "notLoaded": "Error loading results"
  },
  "pt_PT": {
  }
}
</i18n>
