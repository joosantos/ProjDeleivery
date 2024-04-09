<template>
	<div class="absolute inset-0 bg-gray-800">
		<div
			class="absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-xl font-semibold text-white grid grid-cols-1 space-y-4">
			<button
				class="capitalize border rounded-xl border-gray 200 px-2 py-1"
				@click="getDiploma">
				{{ t("getDiplomaAgain") }}
			</button>
			<div class="grid grid-cols-2 grid-rows-2 gap-y-4 gap-x-4">
				<select
					id="selectAthlete"
					v-model="athlete"
					name="selectAthlete"
					class="border rounded-xl border-gray 200 pl-2 pr-10 py-1 bg-gray-800">
					<option v-for="at of athletes" :key="at.id" :value="at.id">
						{{ at.name }}
					</option>
				</select>
				<button
					class="col-span-1 row-span-2 capitalize border rounded-xl border-gray 200 px-2 py-1"
					@click="getSingleDiploma">
					{{ t("getSingleDiploma") }}
				</button>
				<select
					id="selectPlace"
					v-model="place"
					name="selectPlace"
					class="border rounded-xl border-gray 200 pl-2 pr-10 py-1 bg-gray-800">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
				</select>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import store from "@/store";
import { useI18n } from "vue-i18n";
import { getAthleteNameTeam } from "@/services/athlete.service.js";

let { t } = useI18n({ useScope: "global" });
store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);
let athletes = ref([]);
let athlete = ref(null);
let place = ref(3);
const props = defineProps({
	// ID of the tournament
	tournament: {
		type: String,
		required: true,
	},
});
authApi
	.get(`tournaments/${props.tournament}`)
	.then((response) => {
		for (let match of response.data.matches) {
			if (
				match.athlete_red_id != null &&
				athletes.value.findIndex((a) => a.id == match.athlete_red_id) === -1
			) {
				athletes.value.push({
					name: getAthleteNameTeam(match.athlete_red),
					id: match.athlete_red_id,
				});
			}
			if (
				match.athlete_blue_id != null &&
				athletes.value.findIndex((a) => a.id == match.athlete_blue_id) === -1
			) {
				athletes.value.push({
					name: getAthleteNameTeam(match.athlete_blue),
					id: match.athlete_blue_id,
				});
			}
		}
	})
	.catch((e) => {
		console.log(e);
		toast.error(t("error.genericError"));
	});
function getDiploma() {
	authApi
		.get(`tournaments/${props.tournament}/get-diplomas`, { responseType: "blob" })
		.then((response) => {
			const url = URL.createObjectURL(response.data);
			const a = document.createElement("a");
			a.download = "diplomas.pdf";
			a.href = url;
			a.target = "_self";
			a.click();

			setTimeout(function () {
				// For Firefox it is necessary to delay revoking the ObjectURL
				a.remove();
				URL.revokeObjectURL(url);
			}, 100);
			return;
		})
		.catch((e) => {
			console.log(e);
			toast.error(t("error.genericError"));
		});
}
getDiploma();
function getSingleDiploma() {
	if (place.value == null || athlete.value == null) {
		toast.error("error.invalidValues");
		return;
	}

	authApi
		.get(
			`tournaments/${props.tournament}/get-diploma/place/${place.value}/athlete/${athlete.value}`,
			{ responseType: "blob" }
		)
		.then((response) => {
			const url = URL.createObjectURL(response.data);
			const a = document.createElement("a");
			a.download = "diploma.pdf";
			a.href = url;
			a.target = "_self";
			a.click();

			setTimeout(function () {
				// For Firefox it is necessary to delay revoking the ObjectURL
				a.remove();
				URL.revokeObjectURL(url);
			}, 100);
			return;
		})
		.catch((e) => {
			console.log(e);
			toast.error(t("error.genericError"));
		});
}
</script>
