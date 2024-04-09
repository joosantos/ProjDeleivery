<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="max-w-max mx-auto">
		<div class="mx-auto mt-10 text-center text-2xl">
			<p class="text-2xl font-semibold">
				{{ t("athlete") }}
			</p>
			<p class="text-4xl font-bold">
				{{ teamName.name + " (" + teamName.abr + ")" }}
			</p>
			<p class="text-sm font-normal">
				{{ t("note") }}
			</p>
			<p class="">{{ "Tournaments Participated: " + participated.length }}</p>
			<table :class="['w-full mt-10', first.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-[#FFD700] border border-black border-b-0',
						first.length == 0 && 'opacity-50',
					]">
					{{
						t("first", { count: first.length })
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
						t("second", { count: second.length })
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
						t("third", { count: third.length })
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
			<table :class="['w-full mt-10', other.length == 0 && 'opacity-50']">
				<caption
					:class="[
						'font-bold bg-blue-400 border border-black border-b-0',
						other.length == 0 && 'opacity-50',
					]">
					{{
						t("others", { count: other.length })
					}}
				</caption>
				<tr
					v-if="other.length == 0"
					class="bg-blue-100 border border-black divide-y divide-black">
					<div>{{ t("none") }}</div>
				</tr>
				<tr
					v-for="tourn in other"
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
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { unauthApi } from "@/services/api";
import { ref } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
	// ID of the athlete
	team: {
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
let teamName = ref(null);

if (props.team != null) {
	unauthApi
		.get(`competitions/${props.competition}/teams/${props.team}`)
		.then((response) => {
			tournaments.value = response.data;
			for (let tournament of tournaments.value) {
				let participatedFlag = false;
				let aux = null;
				if (
					tournament.first_place_id != null &&
					tournament.first_place.athletes_group[0].athlete.team.id == props.team
				) {
					aux = {
						name: getName(tournament),
						id: tournament.id,
						category: tournament.category.name,
					};
					participated.value.push(aux);
					first.value.push(aux);
					if (teamName.value == null) {
						teamName.value = {
							name: tournament.first_place.athletes_group[0].athlete.team.name,
							abr: tournament.first_place.athletes_group[0].athlete.team.abbreviation,
						};
					}
					participatedFlag = true;
				}
				if (
					tournament.second_place_id != null &&
					tournament.second_place.athletes_group[0].athlete.team.id == props.team
				) {
					aux = {
						name: getName(tournament),
						id: tournament.id,
						category: tournament.category.name,
					};
					if (!participatedFlag) {
						participated.value.push(aux);
						participatedFlag = true;
					}
					second.value.push(aux);
					if (teamName.value == null) {
						teamName.value = {
							name: tournament.second_place.athletes_group[0].athlete.team.name,
							abr: tournament.second_place.athletes_group[0].athlete.team
								.abbreviation,
						};
					}
				}
				if (
					tournament.third_place_id != null &&
					tournament.third_place.athletes_group[0].athlete.team.id == props.team
				) {
					aux = {
						name: getName(tournament),
						id: tournament.id,
						category: tournament.category.name,
					};
					if (!participatedFlag) {
						participated.value.push(aux);
						participatedFlag = true;
					}
					third.value.push(aux);
					if (teamName.value == null) {
						teamName.value = {
							name: tournament.third_place.athletes_group[0].athlete.team.name,
							abr: tournament.third_place.athletes_group[0].athlete.team.abbreviation,
						};
					}
					continue;
				}
				for (let match of tournament.matches) {
					if (
						match.athlete_red_id != null &&
						match.athlete_red.athletes_group[0].athlete.team.id == props.team
					) {
						if (teamName.value == null) {
							teamName.value = {
								name: match.athlete_red.athletes_group[0].athlete.team.name,
								abr: match.athlete_red.athletes_group[0].athlete.team.abbreviation,
							};
						}
						aux = {
							name: getName(tournament),
							id: tournament.id,
							category: tournament.category.name,
						};
						if (!participatedFlag) {
							participated.value.push(aux);
							participatedFlag = true;
							other.value.push(aux);
						}
						break;
					}
					if (
						match.athlete_blue_id != null &&
						match.athlete_blue.athletes_group[0].athlete.team != null &&
						match.athlete_blue.athletes_group[0].athlete.team.id == props.team
					) {
						if (teamName.value == null) {
							teamName.value = {
								name: match.athlete_blue.athletes_group[0].athlete.team.name,
								abr: match.athlete_blue.athletes_group[0].athlete.team.abbreviation,
							};
						}
						aux = {
							name: getName(tournament),
							id: tournament.id,
							category: tournament.category.name,
						};
						if (!participatedFlag) {
							participated.value.push(aux);
							participatedFlag = true;
							other.value.push(aux);
						}
						break;
					}
				}
			}
			loading.value = false;
		})
		.catch(() => {
			toast.error(t("notLoaded"));
		});
}

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
	  "first": "First Place ({count} tournaments)",
	  "second": "Second Place ({count} tournaments)",
	  "third": "Third Place ({count} tournaments)",
	  "others": "Others Place ({count} tournaments)",
	  "athlete": "Results for the Team",
	  "none": "None",
	  "note": "To see the bracket, click on the tournament name",
	  "notLoaded": "Error loading results"
  },
  "pt_PT": {
  }
}
</i18n>
