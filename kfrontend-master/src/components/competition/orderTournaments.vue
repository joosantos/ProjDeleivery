<template>
	<div>
		<NumberMatchesCompetition
			:open="openNumberCombats"
			:competition-id="props.competitionId"
			:competition-name="competition?.name || ''"
			@close="openNumberCombats = false" />
		<div
			class="grid grid-cols-1 grid-cols-2 grid-cols-3 grid-cols-4 grid-cols-5 hidden invisible" />

		<p class="text-3xl font-semibold ml-14">{{ competition?.name }}</p>
		<div
			v-if="loading"
			class="fixed h-screen w-screen top-0 left-0 bg-gray-100 z-50 opacity-50">
			<div class="relative mx-auto top-1/2 -translate-y-1/2">
				<Loading :size="10" />
			</div>
		</div>
		<div class="'relative mt-10'">
			<div class="inline-flex w-full">
				<div class="ml-16">
					<CustomInput
						:type="'text'"
						:mask="'###'"
						:name="'day'"
						:label="t('day')"
						:option-selected="state.day"
						:error="Number(state.day) < 1 ? t('error.day') : ''"
						@value-changed="(option) => (state.day = option)" />
				</div>
				<div
					id="remove"
					class="ml-10 w-[600px] h-14 bg-red-500 border border-black text-center text-white">
					{{ t("dragHere") }}
				</div>
				<div class="ml-auto">
					<SearchSelect
						:title="t('colsNumber')"
						:options="[
							{ id: '1', name: '1' },
							{ id: '2', name: '2' },
							{ id: '3', name: '3' },
							{ id: '4', name: '4' },
							{ id: '5', name: '5' },
						]"
						:option-selected="numberCols"
						:error="''"
						@selected="(option) => (numberCols = option)" />
				</div>
				<div class="relative w-full ml-4 max-w-[300px] mr-24 mt-4">
					<Button
						:message="t('number')"
						type="primary"
						:loading="showSpinningWheel"
						:pill="true"
						:outline="true"
						@button-click="openNumberCombats = true" />
				</div>
			</div>
			<div
				:class="[
					'left-1/2 -translate-x-1/2 relative text-center w-[1750px] mt-4',
					Number(state.day) < 1 && 'opacity-50 pointer-events-none',
				]">
				<p class="w-full text-lg font-medium border border-black border-b-0 bg-blue-300">
					{{ t("morning") }}
				</p>
				<div :class="`justify-between w-full grid grid-cols-${numberCols}`">
					<div
						v-for="item in 12"
						:key="item"
						:class="[
							'w-full min-w-[300px] border border-black',
							item % Number(numberCols) != 0 && 'border-r-0',
							item > 12 - Number(numberCols) ? 'border-b' : 'border-b-0',
						]">
						<p :class="['font-medium bg-gray-200 border-b border-black']">
							{{ t("area", { count: item }) }}
						</p>
						<div :id="'drop' + item + 'M'">
							<div
								:id="item + 'Mp'"
								class="text-green-500 bg-green-100 text-xl font-medium min-h-20 h-full">
								<p>+</p>
								<p>+</p>
							</div>
						</div>
					</div>
				</div>

				<p class="w-full text-lg font-medium border border-black border-y-0 bg-orange-300">
					{{ t("afternoon") }}
				</p>
				<div :class="`justify-between w-full grid grid-cols-${numberCols}`">
					<div
						v-for="item in 12"
						:key="item"
						:class="[
							'w-full min-w-[300px] border border-black',
							item % Number(numberCols) != 0 && 'border-r-0',
							item > 12 - Number(numberCols) ? 'border-b' : 'border-b-0',
						]">
						<p :class="['font-medium bg-gray-200 border-b border-black']">
							{{ t("area", { count: item }) }}
						</p>
						<div :id="'drop' + item + 'A'">
							<div
								:id="item + 'Ap'"
								class="text-green-500 bg-green-100 text-xl font-medium min-h-20 h-full">
								<p>+</p>
								<p>+</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<form
			:class="[
				'flex space-x-6 items-center w-full relative mt-10 px-10',
				Number(state.day) < 1 && 'opacity-50 pointer-events-none',
			]"
			@submit.prevent="numberByArea">
			<div class="ml-4">
				<input
					id="male"
					v-model="state.male"
					name="male"
					type="checkbox"
					@change="sortTourns()" />
				<label for="male" class="ml-1">{{ t("masc") }}</label>
			</div>
			<div>
				<input
					id="female"
					v-model="state.female"
					name="female"
					type="checkbox"
					@change="sortTourns()" />
				<label for="female" class="ml-1">{{ t("fem") }}</label>
			</div>
			<div class="flex flex-col">
				<label for="category" class="ml-1">{{ t("competition.cat") }}</label>
				<input
					id="category"
					v-model="state.category"
					class="border border-black p-0 pl-1"
					name="category"
					type="text"
					@input="sortTourns()" />
			</div>
			<div class="flex flex-col">
				<label for="age" class="ml-1">{{ t("competition.age") }}</label>
				<input
					id="age"
					v-model="state.age"
					class="p-0 pl-1"
					name="age"
					type="number"
					@input="sortTourns()" />
			</div>
			<div class="flex flex-col">
				<label for="name" class="ml-1">{{ t("competition.name") }}</label>
				<input
					id="name"
					v-model="state.name"
					class="p-0 pl-1"
					name="name"
					type="text"
					@input="sortTourns()" />
			</div>
			<div class="flex flex-col">
				<label for="matches" class="ml-1">{{ t("competition.matches") }}</label>

				<input
					id="matches"
					v-model="state.matches"
					class="p-0 pl-1"
					name="matches"
					type="text"
					@input="sortTourns()" />
			</div>
			<div class="flex space-x-2 items-center border border-black p-2 bg-gray-100 rounded-lg">
				<div class="flex flex-col">
					<label for="addArea" class="ml-1">{{ t("competition.addArea") }}</label>
					<input
						id="addArea"
						v-model="state.addArea"
						class="border border-black px-2 w-28"
						name="addArea"
						type="text" />
				</div>

				<div class="flex flex-col">
					<label for="addTime" class="ml-1">{{ t("competition.addTime") }}</label>
					<select
						id="addTime"
						v-model="state.addTime"
						class="p-0 pl-1 w-32"
						name="addTime">
						<option value="M">{{ t("competition.morning") }}</option>
						<option value="A">{{ t("competition.afternoon") }}</option>
					</select>
				</div>

				<div
					class="border border-black p-2 bg-gray-200 cursor-pointer rounded-lg hover:bg-gray-300 active:bg-gray-400 mt-4"
					@click="addAll">
					{{ t("competition.addAll") }}
				</div>
			</div>
		</form>

		<div
			v-if="competition != null"
			id="base"
			:class="[
				'flex flex-wrap gap-1 mt-10 px-10 mb-10',
				Number(state.day) < 1 && 'opacity-50 pointer-events-none',
			]">
			<div
				v-for="tournament in show"
				v-show="
					moreThanOneInscription(tournament) &&
					((tournament.show && tournament.day == null) ||
						(tournament.day != null && tournament.day == state.day))
				"
				:id="tournament.id"
				:key="tournament.id"
				class="bg-purple-200 border border-black px-1 min-w-max text-sm cursor-pointer max-w-[250px] relative">
				{{
					(tournament.order == null ? "" : tournament.order + "º ") + getName(tournament)
				}}
			</div>
		</div>
	</div>
</template>

<script setup>
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import NumberMatchesCompetition from "@/components/competition/modals/numberMatchesCompetition.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import { authApi } from "@/services/api";
import { ref, onMounted, watch } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";
import dragNdrop from "npm-dragndrop";
import { getTournamentName } from "@/services/competition.service.js";

const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});

let { t } = useI18n();
let competition = ref(null);
let show = ref(null);
let numberCols = ref("4");
let state = ref({
	male: true,
	female: true,
	age: "",
	category: "",
	name: "",
	day: "1",
	matches: "",
	addArea: "1",
	addTime: "M",
});
let loading = ref(true);
let showSpinningWheel = ref(false);
let openNumberCombats = ref(false);
const tournamentIDs = ref([]);

watch(
	() => state.value.day,
	() => {
		if (Number(state.value.day) > 0) {
			for (let tourn of show.value) {
				placeTournaments(tourn);
			}
		}
		sortTourns();
	}
);

onMounted(() => {
	authApi
		.get("competitions/" + props.competitionId)
		.then((response) => {
			competition.value = response.data;
			show.value = competition.value.tournaments;
			show.value.sort(function (a, b) {
				if (a.order != b.order) {
					return a.order - b.order;
				}
				if (a.age_min != null) {
					if (b.age_min != null && a.age_min != b.age_min) {
						return a.age_min - b.age_min;
					}
					if (b.age_max != null && a.age_min != b.age_max) {
						return a.age_min - b.age_max;
					}
				} else {
					if (b.age_min != null && a.age_max != b.age_min) {
						return a.age_max - b.age_min;
					}
					if (b.age_max != null && a.age_max != b.age_max) {
						return a.age_max - b.age_max;
					}
				}
				if (a.weight_min == null && a.weight_max == null) {
					if (b.weight_min == null && b.weight_max == null) {
						if (a.is_male) {
							return 1;
						}
						return -1;
					}
					return -1;
				}
				if (b.weight_min == null && b.weight_max == null) {
					return 1;
				}
				if (a.weight_min != null) {
					if (b.weight_min != null && a.weight_min != b.weight_min) {
						return a.weight_min - b.weight_min;
					}
					if (a.weight_min != b.weight_max) {
						return a.weight_min - b.weight_max;
					}
				} else {
					if (b.weight_min != null && a.weight_max != b.weight_min) {
						return a.weight_max - b.weight_min;
					}
					if (a.weight_max != b.weight_max) {
						return a.weight_max - b.weight_max;
					}
				}
				if (a.is_male) {
					return 1;
				}
				return -1;
			});
			setTimeout(() => {
				for (let tourn of show.value) {
					tourn.show = true;
					placeTournaments(tourn);

					dragNdrop({
						element: document.getElementById(tourn.id),
						dropZones: [
							document.getElementById("remove"),
							document.getElementById("drop1M"),
							document.getElementById("drop2M"),
							document.getElementById("drop3M"),
							document.getElementById("drop4M"),
							document.getElementById("drop5M"),
							document.getElementById("drop6M"),
							document.getElementById("drop7M"),
							document.getElementById("drop8M"),
							document.getElementById("drop9M"),
							document.getElementById("drop10M"),
							document.getElementById("drop11M"),
							document.getElementById("drop12M"),
							document.getElementById("drop1A"),
							document.getElementById("drop2A"),
							document.getElementById("drop3A"),
							document.getElementById("drop4A"),
							document.getElementById("drop5A"),
							document.getElementById("drop6A"),
							document.getElementById("drop7A"),
							document.getElementById("drop8A"),
							document.getElementById("drop9A"),
							document.getElementById("drop10A"),
							document.getElementById("drop11A"),
							document.getElementById("drop12A"),
						],
						callback: addDay,
					});
				}
			}, 1000);
			sortTourns();
			loading.value = false;
		})
		.catch(() => {
			toast.error(t("competition.notLoaded"));
			loading.value = false;
		});
});

function placeTournaments(tourn) {
	let drop1M = document.getElementById("drop1M");
	let mp1 = document.getElementById("1Mp");
	let drop2M = document.getElementById("drop2M");
	let mp2 = document.getElementById("2Mp");
	let drop3M = document.getElementById("drop3M");
	let mp3 = document.getElementById("3Mp");
	let drop4M = document.getElementById("drop4M");
	let mp4 = document.getElementById("4Mp");
	let drop5M = document.getElementById("drop5M");
	let mp5 = document.getElementById("5Mp");
	let drop6M = document.getElementById("drop6M");
	let mp6 = document.getElementById("6Mp");
	let drop7M = document.getElementById("drop7M");
	let mp7 = document.getElementById("7Mp");
	let drop8M = document.getElementById("drop8M");
	let mp8 = document.getElementById("8Mp");
	let drop9M = document.getElementById("drop9M");
	let mp9 = document.getElementById("9Mp");
	let drop10M = document.getElementById("drop10M");
	let mp10 = document.getElementById("10Mp");
	let drop11M = document.getElementById("drop11M");
	let mp11 = document.getElementById("11Mp");
	let drop12M = document.getElementById("drop12M");
	let mp12 = document.getElementById("12Mp");
	let drop1A = document.getElementById("drop1A");
	let ap1 = document.getElementById("1Ap");
	let drop2A = document.getElementById("drop2A");
	let ap2 = document.getElementById("2Ap");
	let drop3A = document.getElementById("drop3A");
	let ap3 = document.getElementById("3Ap");
	let drop4A = document.getElementById("drop4A");
	let ap4 = document.getElementById("4Ap");
	let drop5A = document.getElementById("drop5A");
	let ap5 = document.getElementById("5Ap");
	let drop6A = document.getElementById("drop6A");
	let ap6 = document.getElementById("6Ap");
	let drop7A = document.getElementById("drop7A");
	let ap7 = document.getElementById("7Ap");
	let drop8A = document.getElementById("drop8A");
	let ap8 = document.getElementById("8Ap");
	let drop9A = document.getElementById("drop9A");
	let ap9 = document.getElementById("9Ap");
	let drop10A = document.getElementById("drop10A");
	let ap10 = document.getElementById("10Ap");
	let drop11A = document.getElementById("drop11A");
	let ap11 = document.getElementById("11Ap");
	let drop12A = document.getElementById("drop12A");
	let ap12 = document.getElementById("12Ap");
	if (
		tourn.day != null &&
		tourn.morning != null &&
		tourn.area != null &&
		tourn.day == state.value.day
	) {
		let tournDiv = document.getElementById(tourn.id);
		if (tourn.morning) {
			switch (tourn.area) {
				case "1":
					tournDiv.classList.add("mx-auto");
					drop1M.appendChild(tournDiv);
					drop1M.appendChild(mp1);
					break;
				case "2":
					tournDiv.classList.add("mx-auto");
					drop2M.appendChild(tournDiv);
					drop2M.appendChild(mp2);
					break;
				case "3":
					tournDiv.classList.add("mx-auto");
					drop3M.appendChild(tournDiv);
					drop3M.appendChild(mp3);
					break;
				case "4":
					tournDiv.classList.add("mx-auto");
					drop4M.appendChild(tournDiv);
					drop4M.appendChild(mp4);
					break;
				case "5":
					tournDiv.classList.add("mx-auto");
					drop5M.appendChild(tournDiv);
					drop5M.appendChild(mp5);
					break;
				case "6":
					tournDiv.classList.add("mx-auto");
					drop6M.appendChild(tournDiv);
					drop6M.appendChild(mp6);
					break;
				case "7":
					tournDiv.classList.add("mx-auto");
					drop7M.appendChild(tournDiv);
					drop7M.appendChild(mp7);
					break;
				case "8":
					tournDiv.classList.add("mx-auto");
					drop8M.appendChild(tournDiv);
					drop8M.appendChild(mp8);
					break;
				case "9":
					tournDiv.classList.add("mx-auto");
					drop9M.appendChild(tournDiv);
					drop9M.appendChild(mp9);
					break;
				case "10":
					tournDiv.classList.add("mx-auto");
					drop10M.appendChild(tournDiv);
					drop10M.appendChild(mp10);
					break;
				case "11":
					tournDiv.classList.add("mx-auto");
					drop11M.appendChild(tournDiv);
					drop11M.appendChild(mp11);
					break;
				case "12":
					tournDiv.classList.add("mx-auto");
					drop12M.appendChild(tournDiv);
					drop12M.appendChild(mp12);
					break;
			}
		} else {
			switch (tourn.area) {
				case "1":
					tournDiv.classList.add("mx-auto");
					drop1A.appendChild(tournDiv);
					drop1A.appendChild(ap1);
					break;
				case "2":
					tournDiv.classList.add("mx-auto");
					drop2A.appendChild(tournDiv);
					drop2A.appendChild(ap2);
					break;
				case "3":
					tournDiv.classList.add("mx-auto");
					drop3A.appendChild(tournDiv);
					drop3A.appendChild(ap3);
					break;
				case "4":
					tournDiv.classList.add("mx-auto");
					drop4A.appendChild(tournDiv);
					drop4A.appendChild(ap4);
					break;
				case "5":
					tournDiv.classList.add("mx-auto");
					drop5A.appendChild(tournDiv);
					drop5A.appendChild(ap5);
					break;
				case "6":
					tournDiv.classList.add("mx-auto");
					drop6A.appendChild(tournDiv);
					drop6A.appendChild(ap6);
					break;
				case "7":
					tournDiv.classList.add("mx-auto");
					drop7A.appendChild(tournDiv);
					drop7A.appendChild(ap7);
					break;
				case "8":
					tournDiv.classList.add("mx-auto");
					drop8A.appendChild(tournDiv);
					drop8A.appendChild(ap8);
					break;
				case "9":
					tournDiv.classList.add("mx-auto");
					drop9A.appendChild(tournDiv);
					drop9A.appendChild(ap9);
					break;
				case "10":
					tournDiv.classList.add("mx-auto");
					drop10A.appendChild(tournDiv);
					drop10A.appendChild(ap10);
					break;
				case "11":
					tournDiv.classList.add("mx-auto");
					drop11A.appendChild(tournDiv);
					drop11A.appendChild(ap11);
					break;
				case "12":
					tournDiv.classList.add("mx-auto");
					drop12A.appendChild(tournDiv);
					drop12A.appendChild(ap12);
					break;
			}
		}
	}
}

async function addDay(obj) {
	loading.value = true;
	obj.element.style = null;
	if (obj.dropped) {
		let tourn = competition.value.tournaments.find((a) => a.id == obj.element.id);
		if (tourn == null) {
			toast.error(t("tournNull"));
			loading.value = false;
			return;
		}
		let promises = [];

		if (obj.dropped[0].id == "remove") {
			promises.push(
				authApi
					.put("tournaments/" + tourn.id, {
						day: null,
						morning: null,
						area: null,
						order: null,
					})
					.then((response) => {
						show.value[show.value.findIndex((a) => a.id == response.data.id)] =
							response.data;
					})
			);
			let areaDiv = obj.element.parentNode;
			obj.element.classList.remove("mx-auto");
			document.getElementById("base").appendChild(obj.element);
			Promise.all(promises).then(() => {
				orderInArea(areaDiv).then(() => {
					loading.value = false;
				});
			});
			return;
		}
		promises.push(
			authApi
				.put("tournaments/" + tourn.id, {
					day: state.value.day,
					morning: obj.dropped[0].id.indexOf("M") != -1,
					area: obj.dropped[0].id.replace("drop", "").replace("A", "").replace("M", ""),
				})
				.then((response) => {
					show.value[show.value.findIndex((a) => a.id == response.data.id)] =
						response.data;
				})
		);
		obj.element.classList.add("mx-auto");
		let plusObj = obj.dropped[0].childNodes[obj.dropped[0].childElementCount - 1];
		obj.dropped[0].appendChild(obj.element);
		obj.dropped[0].appendChild(plusObj);
		Promise.all(promises).then(() => {
			orderInArea(obj.dropped[0]).then(() => {
				loading.value = false;
			});
		});
	} else {
		loading.value = false;
	}
}

async function orderInArea(areaDiv) {
	let idList = [];
	for (let tournDiv of areaDiv.childNodes) {
		if (tournDiv.style.display != "none") {
			let tournAux = competition.value.tournaments.find((a) => a.id == tournDiv.id);
			if (tournAux == null) {
				continue;
			}
			idList.push(tournAux.id);
		}
	}

	return authApi
		.put(
			`competitions/${competition.value.id}/tournaments/order/${state.value.day}/${
				areaDiv.id.indexOf("M") != -1
			}/${areaDiv.id.replace("drop", "").replace("A", "").replace("M", "")}`,
			{ ids: idList }
		)
		.then((response) => {
			for (let tournament of competition.value.tournaments) {
				for (let tournamentUpdated of response.data) {
					if (tournament.id == tournamentUpdated.id) {
						tournament.order = tournamentUpdated.order;
					}
				}
			}
		});
}

function sortTourns() {
	for (let tourn of show.value) {
		if (
			tourn.matches.length == 1 &&
			tourn.matches[0].athlete_blue == null &&
			tourn.category.category_type == "Tournament"
		) {
			tourn.show = false;
			continue;
		}
		if (!state.value.male && tourn.is_male) {
			tourn.show = false;
			continue;
		}
		if (!state.value.female && !tourn.is_male) {
			tourn.show = false;
			continue;
		}
		if (
			state.value.age != "" &&
			(tourn.age_min > state.value.age || tourn.age_max < state.value.age)
		) {
			tourn.show = false;
			continue;
		}
		if (
			state.value.category != "" &&
			tourn.category.name.toUpperCase().indexOf(state.value.category.toUpperCase()) == -1
		) {
			tourn.show = false;
			continue;
		}
		if (
			state.value.name != "" &&
			getName(tourn).toUpperCase().indexOf(state.value.name.toUpperCase()) == -1
		) {
			tourn.show = false;
			continue;
		}
		if (state.value.matches != "" && !isNaN(Number(state.value.matches))) {
			if (tourn.matches.length != Number(state.value.matches)) {
				tourn.show = false;
				continue;
			}
		}
		tourn.show = true;
	}
}

function getName(tourn) {
	let name = getTournamentName(tourn, t);
	name = name
		.replace("Adaptado", "Ad.")
		.replace("Adapted", "Ad.")
		.replace("Desportivo", "Des.")
		.replace("com", "c/");
	let len = 0;
	if (tourn.inscriptions == null || tourn.inscriptions.length === 0) {
		if (tourn.matches != null) {
			len = tourn.matches.length;
		}
	} else {
		for (let inscription of tourn.inscriptions) {
			if (inscription.confirmed && inscription.accepted) {
				len += 1;
			}
		}
	}
	name += ` (${len})`;

	return name;
}

function numberByArea() {
	showSpinningWheel.value = true;
	authApi
		.get("competitions/" + props.competitionId + "/number-matches")
		.then(() => {
			showSpinningWheel.value = false;
			toast.success(t("combatsNumbered"));
		})
		.catch(() => {
			toast.error(t("combatsNotNumbered"));
			showSpinningWheel.value = false;
		});
}

function addAll() {
	loading.value = true;
	if (isNaN(Number(state.value.addArea)) || Number(state.value.addArea) > 10) {
		toast.error("Area number invalid");
		loading.value = false;
		return;
	}

	let promises = [];
	let dropZone = document.getElementById("drop" + state.value.addArea + state.value.addTime);
	let plusDiv = document.getElementById(state.value.addArea + state.value.addTime + "p");
	for (let tourn of show.value) {
		if (tourn.show && tourn.day == null) {
			let tournDiv = document.getElementById(tourn.id);
			promises.push(
				authApi
					.put("tournaments/" + tourn.id, {
						day: state.value.day,
						morning: state.value.addTime == "M",
						area: state.value.addArea,
						order: dropZone.childElementCount,
					})
					.then((response) => {
						show.value[show.value.findIndex((a) => a.id == response.data.id)] =
							response.data;
					})
			);
			tournDiv.classList.add("mx-auto");
			dropZone.appendChild(tournDiv);
			dropZone.appendChild(plusDiv);
		}
	}
	Promise.all(promises).then(() => {
		loading.value = false;
	});
}

function moreThanOneInscription(tourn) {
	let len = 0;
	if (tourn.inscriptions == null || tourn.inscriptions.length === 0) {
		if (tourn.matches != null) {
			return tourn.matches.length > 0;
		}
	} else {
		for (let inscription of tourn.inscriptions) {
			if (inscription.confirmed && inscription.accepted) {
				len += 1;
			}
		}
	}
	return len > 1;
}
</script>

<i18n>
{
	"en_GB": {
		"colsNumber": "Number of columns",
		"error": {
			"day": "Invalid day"
		},
		"masc": "Masc.",
		"fem": "Fem.",
		"open": "Open",
		"year": "{count} Year | {count} Years",
        "day": "Day",
        "tournNull": "Error sending data, please refresh the page",
        "dragHere": "Drag here to remove from table",
		"combatsNumbered": "Combats numbered",
		"combatsNotNumbered": "It wasn't possible to number the combats",
		"area": "Area {count}",
		"morning": "Morning",
		"afternoon": "Afternoon",
		"number": "Number Combats",
		"competition": {
			"notLoaded": "Wasn't possible to load the competition",
			"title": "Competitions",
			"cat": "Category",
			"name": "Name",
			"age": "Age",
			"area": "Area {count}",
			"areaLabel": "Area",
			"noArea": "Without Area",
			"update": "Number combats by Area",
			"matches": "Number of matches",
			"addAll": "Add all showing",
			"addArea": "Add all to area",
			"addTime": "Time of the day",
			"morning": "Morning",
			"afternoon": "Afternoon",
		},
		"table": {
			"name": "Name",
			"matches": "Nº Matches",
			"preview": "Show Tournament",
			"edit": "Edit Tournament"
		},
		"belts": {
			"white": "White",
			"white-yellow": "White and Yellow",
			"yellow": "Yellow",
			"yellow-orange": "Yellow and Orange",
			"orange": "Orange",
			"orange-purple": "Orange and Purple",
			"purple": "Purple",
			"purple-blue": "Purple and Blue",
			"blue": "Blue",
			"blue-green": "Blue and Green",
			"green": "Green",
			"brown-jr": "Brown Junior",
			"brown": "Brown",
			"black-jr": "Black Junior",
			"black": "Black",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
	"pt_PT": {
		"colsNumber": "Número de colunas",
		"error": {
			"day": "Dia inválido"
		},
		"masc": "Masc.",
		"fem": "Fem.",
		"open": "Open",
		"year": "{count} Ano | {count} Anos",
		"competition": {
			"age": "Idade",
			"area": "Área {count}",
			"areaLabel": "Área",
			"noArea": "Sem Área",
			"update": "Numerar combates por Área"
		},
		"table": {
			"name": "Nome",
			"matches": "Nº Combates",
			"preview": "Mostrar Torneio",
			"edit": "Editar Torneio"
		},
		"belts": {
			"white": "Branco",
			"white-yellow": "Branco e Amarelo",
			"yellow": "Amarelo",
			"yellow-orange": "Amarelo e Laranja",
			"orange": "Laranja",
			"orange-purple": "Laranja e Púrpura",
			"purple": "Púrpura",
			"purple-blue": "Púrpura e Azul",
			"blue": "Azul",
			"blue-green": "Azul e Verde",
			"green": "Verde",
			"brown-jr": "Castanho Junior",
			"brown": "Castanho",
			"black-jr": "Preto Junior",
			"black": "Preto",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	}
}
</i18n>
