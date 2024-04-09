<template>
	<div class="grid grid-cols-12 gap-6">
		<div class="col-span-12">
			<h1 class="text-3xl font-semibold">{{ t("createStickers") }}</h1>
		</div>
		<div class="col-span-12 grid grid-cols-12 gap-6" @keypress.enter.prevent="createDoc">
			<div class="col-span-12 md:col-span-3">
				<CustomInput
					:label="t('form.year')"
					type="text"
					mask="####"
					:name="'year'"
					:option-selected="year"
					:error="yearError"
					@value-changed="(option) => (year = option.toUpperCase())" />
			</div>
			<div class="col-span-12 md:col-span-3 mt-auto">
				<Button
					:message="t('form.open')"
					type="primary"
					:submit="false"
					:loading="docLoading"
					@click.prevent="createDoc" />
			</div>
		</div>
		<div
			class="col-start-1 md:col-start-1 col-span-12 md:col-span-6"
			@keypress.enter.prevent="searchAthletes">
			<CustomInput
				:label="t('form.name')"
				type="text"
				:name="'name'"
				:option-selected="nameSearch"
				:error="nameSearchError"
				@value-changed="(option) => (nameSearch = option)" />
		</div>
		<div class="col-span-12 md:col-span-6 lg:col-span-3 mt-auto">
			<Button
				:message="t('form.search')"
				:loading="loadingAthletes"
				type="primary"
				:submit="false"
				@button-click="searchAthletes" />
		</div>
		<div class="col-span-12 md:col-span-6" @keypress.enter.prevent="searchAthletesByTeam">
			<CustomInput
				:label="t('form.team')"
				type="text"
				:name="'team'"
				:option-selected="teamSearch"
				:error="teamSearchError"
				@value-changed="(option) => (teamSearch = option.toUpperCase())" />
		</div>
		<div class="col-span-12 md:col-span-6 lg:col-span-3 mt-auto">
			<Button
				:message="t('form.search')"
				:loading="loadingAthletesTeam"
				type="primary"
				:submit="false"
				@button-click="searchAthletesByTeam" />
		</div>

		<div class="col-span-12 md:col-span-6">
			<p class="text-center font-medium text-xl">{{ t("athletes.search") }}</p>
		</div>
		<div class="hidden md:block md:col-span-6">
			<p class="text-center font-medium text-xl">{{ t("athletes.create") }}</p>
		</div>
		<div
			class="md:col-start-1 lg:col-start-1 col-span-12 md:col-span-6 bg-gray-100 min-h-[4rem] rounded border border-gray-300 px-2 py-2">
			<div v-for="athlete of athletes" :key="athlete.id" class="flex">
				<button
					v-show="athlete.show"
					class="inline-flex px-2 py-px hover:bg-gray-300 cursor-pointer rounded w-full group"
					@click.prevent="addAthlete(athlete)">
					<p>
						{{
							t("fedNum", {
								num: athlete?.private_info?.federation_number
									?.toString()
									.padStart(5, "0"),
							})
						}}
					</p>
					<p class="ml-2">
						{{ athlete.name }}
					</p>
					<p v-if="athlete.team" class="ml-2">
						{{ `(${athlete.team.abbreviation})` }}
					</p>
					<div class="ml-auto mt-1 invisible group-hover:visible">
						<ArrowRightIcon class="w-4 h-4 hidden md:block" />
						<ArrowDownIcon class="w-4 h-4 block md:hidden" />
					</div>
				</button>
			</div>
		</div>
		<div class="block md:hidden col-span-12">
			<p class="text-center font-medium text-xl">{{ t("athletes.create") }}</p>
		</div>
		<div
			class="col-span-12 md:col-span-6 bg-gray-100 min-h-[4rem] rounded border border-gray-300 px-2 py-2">
			<div
				v-for="(athlete, index) of athletesToCreateStickers"
				:key="athlete.id"
				class="flex">
				<button
					class="inline-flex px-2 py-px hover:bg-gray-300 cursor-pointer rounded w-full group"
					@click.prevent="removeAthlete(athlete, index)">
					<p>
						{{ `${index + 1}º -` }}
					</p>
					<p class="ml-2">
						{{
							t("fedNum", {
								num: athlete?.private_info?.federation_number
									?.toString()
									.padStart(5, "0"),
							})
						}}
					</p>
					<p class="ml-2">
						{{ athlete.name }}
					</p>
					<p v-if="athlete.team" class="ml-2">
						{{ `(${athlete.team.abbreviation})` }}
					</p>
					<div class="ml-auto mt-1 invisible group-hover:visible">
						<ArrowLeftIcon class="w-4 h-4 hidden md:block" />
						<ArrowUpIcon class="w-4 h-4 block md:hidden" />
					</div>
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ArrowUpIcon, ArrowRightIcon, ArrowDownIcon, ArrowLeftIcon } from "@heroicons/vue/24/solid";
import Button from "@/components/partials/button.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref } from "vue";
import { authApi, errorHandling, translateDateFromApi } from "@/services/api";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { jsPDF } from "jspdf";
import QRCode from "qrcode";

let { t } = useI18n();
let loadingAthletes = ref(false);
let loadingAthletesTeam = ref(false);
let nameSearch = ref("");
let teamSearch = ref("");
let nameSearchError = ref("");
let teamSearchError = ref("");
let athletesToCreateStickers = ref([]);
let athletes = ref([]);
let year = ref(`${new Date(Date.now()).getFullYear()}`);
let yearError = ref("");
let docLoading = ref(false);
let doc = new jsPDF({
	orientation: "p",
	unit: "mm",
	format: "a4",
	putOnlyUsedFonts: true,
	floatPrecision: 16,
});

function searchAthletes() {
	nameSearchError.value = "";
	if (nameSearch.value.trim() == "") {
		nameSearchError.value = t("error.required");
		return;
	}
	loadingAthletes.value = true;
	authApi
		.get(`athletes/name/${nameSearch.value.trim()}`)
		.then((response) => {
			athletes.value = response.data;
			for (let athlete of athletes.value) {
				let index = athletesToCreateStickers.value.findIndex((a) => a.id === athlete.id);
				athlete.show = index === -1;
			}
			loadingAthletes.value = false;
		})
		.catch((error) => {
			errorHandling(error);
			loadingAthletes.value = false;
		});
}

function searchAthletesByTeam() {
	teamSearchError.value = "";
	if (teamSearch.value.trim() == "") {
		teamSearchError.value = t("error.required");
		return;
	}
	loadingAthletesTeam.value = true;
	authApi
		.get(`athletes/team/abbreviation/${teamSearch.value.trim()}`)
		.then((response) => {
			athletes.value = response.data;
			for (let athlete of athletes.value) {
				let index = athletesToCreateStickers.value.findIndex((a) => a.id === athlete.id);
				athlete.show = index === -1;
			}
			loadingAthletesTeam.value = false;
		})
		.catch((error) => {
			loadingAthletesTeam.value = false;
			errorHandling(error);
		});
}

function addAthlete(athlete) {
	athlete.show = false;
	athletesToCreateStickers.value.push(athlete);
}

function removeAthlete(athlete, index) {
	let athletesIndex = athletes.value.findIndex((a) => a.id === athlete.id);
	if (athletesIndex !== -1) {
		athletes.value.find((a) => a.id === athlete.id).show = true;
	}
	athletesToCreateStickers.value.splice(index, 1);
}

function createDoc() {
	yearError.value = "";
	if (!year.value.match(/^\d{4}/g)) {
		yearError.value = t("error.year");
		return;
	}
	docLoading.value = true;
	doc = new jsPDF({
		orientation: "p",
		unit: "mm",
		format: "a4",
		putOnlyUsedFonts: true,
		floatPrecision: 16,
	});
	let index = 0;
	let startX = 5;
	let startY = -10;
	for (let athlete of athletesToCreateStickers.value) {
		if (index % 70 === 0 && index !== 0) {
			doc.addPage("a4", "p");
			startX = 0;
			startY = 10;
		} else {
			if (index % 5 === 0) {
				startX = 0;
				startY += 25;
			} else {
				startX += 42;
			}
		}
		doc.setTextColor("0.00", "0.00", "0.00");
		doc.setFont("helvetica", "normal", "normal");
		// Rectangle
		doc.rect(startX, startY, 42, 25);
		// Image
		doc.addImage("/sticker.jpg", "JPEG", startX + 1, startY + 1, 40, 3);
		// Name
		doc.setFontSize(5);
		doc.setFont("helvetica", "normal", "bold");
		doc.text(getName(athlete.name), startX + 2, startY + 6);
		// Public Utility
		doc.setFontSize(2);
		doc.text("UTILIDADE PUBLICA DESPORTIVA", startX + 2, startY + 1.5, {
			maxWidth: 10,
		});
		// Birhtday
		doc.setFontSize(4);
		doc.setFont("helvetica", "normal", "normal");
		doc.text(`DN. ${translateDateFromApi(athlete.birthday)}`, startX + 2, startY + 7.5);
		// Fed Num
		doc.text(
			`Atleta Nº ${athlete.private_info.federation_number.toString().padStart(5, "0")}`,
			startX + 31.5,
			startY + 7.5
		);
		// Club
		if (athlete?.team?.name) {
			doc.text(`Clube - ${athlete.team.name}`, startX + 2, startY + 9, {
				maxWidth: 30,
			});
		}
		// Year
		doc.setFontSize(4);
		doc.setTextColor("1.00", "0.00", "0.00");
		doc.setFont("helvetica", "normal", "bold");
		doc.text(year.value, startX + 38.2, startY + 6);
		// QRCode
		let qrcodeUrl = new URL(
			router.resolve({ name: "Athlete Page", params: { athleteId: athlete.id } }).href,
			window.location.origin
		).href;
		QRCode.toDataURL(
			qrcodeUrl,
			{ version: 5, errorCorrectionLevel: "M", margin: 0 },
			(err, url) => {
				if (err != null) console.log(err);
				doc.addImage(url, "PNG", startX + 14, startY + 10.7, 14, 14);
			}
		);
		index += 1;
	}
	doc.save("vinhetas.pdf");
	docLoading.value = false;
}

function getName(name) {
	let split = name.split(" ");
	if (split.length === 1) return split[0].toUpperCase();
	return `${split[0].toUpperCase()} ${split[split.length - 1].toUpperCase()}`;
}
</script>

<i18n>
{
	"en_GB": {
		"form": {
            "name": "Search Athlete By Name",
            "team": "Search Athletes By Team",
            "search": "Search Athletes",
			"year": "Year (YYYY)",
			"open": "Open PDF"
		},
		"athletes": {
			"search": "Athletes Searched",
			"create": "Atlhetes To Create Stickers",
		},
        "error": {
            "required": "Cannot be empty",
			"year": "Invalid Year"
		},
		"createStickers": "Create Stickers",
        "fedNum": "Nº. {num}",
	},
	"pt_PT": {
	}
}
</i18n>
