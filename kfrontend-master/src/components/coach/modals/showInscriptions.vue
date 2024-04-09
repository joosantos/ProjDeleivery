<template>
	<Modal
		:open="props.open"
		:outside-click="true"
		:show-x="true"
		size="5xl"
		@close="emit('close')">
		<Loading v-if="loading" :size="10" />
		<div v-else>
			<!-- Competition name -->
			<p class="text-3xl font-semibold text-center">
				{{ props.competitionName }}
			</p>

			<!-- Show inscriptions by athlete or tournament -->
			<RadioGroup v-if="inscriptionsAthlete.length" v-model="showAthleteInscriptions">
				<div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4">
					<RadioGroupOption v-slot="{ checked, active }" as="template" :value="true">
						<div
							:class="[
								checked ? 'border-transparent' : 'border-gray-300',
								active ? 'border-indigo-500 ring-2 ring-indigo-500' : '',
								'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
							]">
							<span class="flex flex-1">
								<span class="flex flex-col">
									<RadioGroupLabel
										as="span"
										class="block text-sm font-medium text-gray-900">
										{{ t("showIncriptionsByAthlete") }}
									</RadioGroupLabel>
								</span>
							</span>
							<CheckCircleIcon
								:class="[!checked ? 'invisible' : '', 'h-5 w-5 text-indigo-600']"
								aria-hidden="true" />
							<span
								:class="[
									active ? 'border' : 'border-2',
									checked ? 'border-indigo-500' : 'border-transparent',
									'pointer-events-none absolute -inset-px rounded-lg',
								]"
								aria-hidden="true" />
						</div>
					</RadioGroupOption>
					<RadioGroupOption v-slot="{ checked, active }" as="template" :value="false">
						<div
							:class="[
								checked ? 'border-transparent' : 'border-gray-300',
								active ? 'border-indigo-500 ring-2 ring-indigo-500' : '',
								'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
							]">
							<span class="flex flex-1">
								<span class="flex flex-col">
									<RadioGroupLabel
										as="span"
										class="block text-sm font-medium text-gray-900">
										{{ t("showIncriptionsByTournaments") }}
									</RadioGroupLabel>
								</span>
							</span>
							<CheckCircleIcon
								:class="[!checked ? 'invisible' : '', 'h-5 w-5 text-indigo-600']"
								aria-hidden="true" />
							<span
								:class="[
									active ? 'border' : 'border-2',
									checked ? 'border-indigo-500' : 'border-transparent',
									'pointer-events-none absolute -inset-px rounded-lg',
								]"
								aria-hidden="true" />
						</div>
					</RadioGroupOption>
				</div>
			</RadioGroup>

			<!-- Button to copy inscriptions list -->
			<Button
				class="max-w-max mt-2"
				:message="t('copyListOfInscriptionsAccepted')"
				type="success"
				size="small"
				@button-click="copyList" />

			<!-- If no inscriptions -->
			<div v-if="!inscriptionsAthlete.length" class="font-semibold text-center text-xl">
				<p>{{ t("noInscriptionsToShow") }}</p>
			</div>

			<!-- Get payment guide and upload payment comprovative -->
			<div v-if="inscriptionsAthlete.length" class="mb-2 mt-1 justify-between flex">
				<div v-if="selectForPaymentComprovative" class="inline-flex space-x-2">
					<Button
						class="max-w-max"
						:message="t('sendPaymentComprovative')"
						type="success"
						:loading="loadingSendingPaymentComprovative"
						@button-click="sendPaymentComprovative" />
					<FileInput
						:name="'paymentComprovative'"
						:label="t('paymentComprovative')"
						:error="''"
						@value-changed="(option) => (paymentComprovative = option)" />
				</div>
				<div class="space-x-2">
					<Button
						v-if="!selectForPaymentComprovative"
						class="max-w-max"
						:message="
							selectForPaymentGuide
								? t('cancel')
								: t('selectInscriptionsForPaymentGuide')
						"
						:type="selectForPaymentGuide ? 'danger' : 'primary'"
						@button-click="selectForPaymentGuide = !selectForPaymentGuide" />
					<Button
						v-if="selectForPaymentGuide"
						class="max-w-max"
						:message="t('selectAll')"
						size="small"
						type="primary"
						@button-click="selectAllForPaymentGuide" />
					<Button
						v-if="selectForPaymentGuide"
						class="max-w-max"
						:message="t('unselectAll')"
						size="small"
						type="primary"
						@button-click="selectedForPaymentGuide = []" />
				</div>
				<div class="space-x-2">
					<Button
						v-if="selectForPaymentComprovative"
						class="max-w-max"
						:message="t('selectAll')"
						size="small"
						type="primary"
						@button-click="selectAllForPaymentComprovative" />
					<Button
						v-if="selectForPaymentComprovative"
						class="max-w-max"
						:message="t('unselectAll')"
						size="small"
						type="primary"
						@button-click="selectedForPaymentComprovative = []" />
					<Button
						v-if="!selectForPaymentGuide"
						class="max-w-max"
						:message="
							selectForPaymentComprovative
								? t('cancel')
								: t('selectInscriptionsToSendPaymentComprovative')
						"
						:type="selectForPaymentComprovative ? 'danger' : 'primary'"
						@button-click="
							selectForPaymentComprovative = !selectForPaymentComprovative
						" />
				</div>
				<Button
					v-if="selectForPaymentGuide"
					class="max-w-max"
					:message="t('getPaymentGuide')"
					type="success"
					:loading="loadingDownloadPaymentGuide"
					@button-click="getPaymentGuide" />
			</div>

			<!-- Show inscriptions by athlete -->
			<div v-if="showAthleteInscriptions" class="space-y-4">
				<div v-for="athlete of inscriptionsAthlete" :key="athlete.id" class="space-y-0.5">
					<p class="font-semibold text-lg">
						{{
							`${athlete.name} - - - ${athlete.tournaments.length} ${t(
								"tournament",
								athlete.tournaments.length
							)}`
						}}
					</p>
					<div
						v-for="tournament of athlete.tournaments"
						:key="tournament.tournament_id"
						@click="
							selectForPaymentGuide
								? toogleSelectedForPaymentGuide(
										athlete.id,
										tournament.tournament_id
								  )
								: selectForPaymentComprovative
								? toogleSelectedForPaymentComprovative(
										athlete.id,
										tournament.tournament_id
								  )
								: null
						"
						:class="[
							'inline-flex w-full rounded-xl px-2',
							selectForPaymentGuide
								? selectedForPaymentGuide.findIndex(
										(a) =>
											a.athlete_competition_id === athlete.id &&
											a.tournament_id === tournament.tournament_id
								  ) === -1
									? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
									: 'bg-yellow-300 border-yellow-500 hover:bg-yellow-400'
								: '',
							selectForPaymentComprovative
								? selectedForPaymentComprovative.findIndex(
										(a) =>
											a.athlete_competition_id === athlete.id &&
											a.tournament_id === tournament.tournament_id
								  ) === -1
									? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
									: 'bg-green-300 border-green-500 hover:bg-green-400'
								: '',
							(selectForPaymentGuide || selectForPaymentComprovative) &&
								'cursor-pointer',
						]">
						<p>{{ tournament.name }}</p>

						<a
							v-if="tournament.payment_comprovative_url"
							class="min-w-max link ml-auto"
							target="_blank"
							:href="
								'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
								tournament.payment_comprovative_url
							">
							{{ t("seePaymentComprovative") }}
						</a>
						<div
							:class="[
								'inline-flex rounded-full px-2',
								tournament.payment_comprovative_url ? 'ml-2' : 'ml-auto',
							]">
							<p v-if="tournament.accepted" class="text-green-500">
								{{ t("accepted") }}
							</p>
							<p v-else class="text-red-500">{{ t("notAccepted") }}</p>
						</div>
						<div
							v-if="!selectForPaymentGuide && !selectForPaymentComprovative"
							class="inline-flex text-red-500 rounded-full cursor-pointer hover:bg-red-200 px-2 ml-2"
							@click="deleteInscription(athlete.id, tournament.tournament_id)">
							<p>{{ t("remove") }}</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Show inscriptions by tournament -->
			<div v-else class="space-y-4">
				<div v-for="tournament of inscriptionsTournament" :key="tournament.id">
					<p class="font-semibold text-lg">
						{{
							`${tournament.name} - - - ${tournament.athletes.length} ${t(
								"athlete.self",
								tournament.athletes.length
							)}`
						}}
					</p>
					<div
						v-for="athlete of tournament.athletes"
						:key="athlete.athlete_id"
						@click="
							selectForPaymentGuide
								? toogleSelectedForPaymentGuide(athlete.athlete_id, tournament.id)
								: selectForPaymentComprovative
								? toogleSelectedForPaymentComprovative(
										athlete.athlete_id,
										tournament.id
								  )
								: null
						"
						:class="[
							'inline-flex w-full rounded-xl px-2',
							selectForPaymentGuide
								? selectedForPaymentGuide.findIndex(
										(a) =>
											a.athlete_competition_id === athlete.athlete_id &&
											a.tournament_id === tournament.id
								  ) === -1
									? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
									: 'bg-yellow-300 border-yellow-500 hover:bg-yellow-400'
								: '',
							selectForPaymentComprovative
								? selectedForPaymentComprovative.findIndex(
										(a) =>
											a.athlete_competition_id === athlete.athlete_id &&
											a.tournament_id === tournament.id
								  ) === -1
									? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
									: 'bg-green-300 border-green-500 hover:bg-green-400'
								: '',
							(selectForPaymentGuide || selectForPaymentComprovative) &&
								'cursor-pointer',
						]">
						>
						<div class="flex w-full">
							<p class="max-w-max">
								{{ `${getAthleteNameTeam(athlete.athlete)}` }}
							</p>
							<a
								v-if="athlete.payment_comprovative_url"
								class="min-w-max link ml-auto"
								target="_blank"
								:href="
									'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
									athlete.payment_comprovative_url
								">
								{{ t("seePaymentComprovative") }}
							</a>
							<div
								:class="[
									'inline-flex rounded-full px-2',
									athlete.payment_comprovative_url ? 'ml-2' : 'ml-auto',
								]">
								<p v-if="athlete.accepted" class="text-green-500">
									{{ t("accepted") }}
								</p>
								<p v-else class="text-red-500">{{ t("notAccepted") }}</p>
							</div>
							<div
								v-if="!selectForPaymentGuide && !selectForPaymentComprovative"
								class="inline-flex text-red-500 rounded-full cursor-pointer hover:bg-red-200 px-2 ml-2"
								@click="deleteInscription(athlete.athlete_id, tournament.id)">
								<p>{{ t("remove") }}</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- List hidden to be copied -->
			<CopyAccepted
				:inscriptions-tournament="inscriptionsTournament"
				:inscriptions-athletes="inscriptionsAthlete"
				@copy-list-html-tournaments="(option) => (copyListHtmlTournaments = option)"
				@copy-list-html-athletes="(option) => (copyListHtmlAthletes = option)" />
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import CopyAccepted from "@/components/competition/partials/copyAccepted.vue";
import Button from "@/components/partials/button.vue";
import Loading from "@/components/partials/loading.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import toast from "@/toast.js";
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";
import { CheckCircleIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	competitionId: {
		type: String,
		required: true,
	},
	competitionName: {
		type: String,
		required: true,
	},
	teamId: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close", "created", "updated"]);

const loading = ref(false);
const inscriptions = ref([]);
const inscriptionsTournament = ref([]);
const inscriptionsAthlete = ref([]);
const showAthleteInscriptions = ref(true);
const selectForPaymentGuide = ref(false);
const selectedForPaymentGuide = ref([]);
const loadingDownloadPaymentGuide = ref(false);
const selectForPaymentComprovative = ref(false);
const selectedForPaymentComprovative = ref([]);
const loadingSendingPaymentComprovative = ref(false);
const paymentComprovative = ref(null);
const copyListHtmlTournaments = ref(null);
const copyListHtmlAthletes = ref(null);

watch(
	() => props.open,
	(after) => {
		if (after) getInscriptions();
	}
);

const getInscriptions = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.get(
			`inscriptions?competition_id=${props.competitionId}&team_id=${props.teamId}&inscription_confirmed=true&limit=-1`
		);
		inscriptions.value = data.results;
		groupInscriptions();
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

const groupInscriptions = () => {
	inscriptionsTournament.value = [];
	inscriptionsAthlete.value = [];
	for (const inscription of inscriptions.value) {
		const tournName = getTournamentName(inscription.tournament, t);
		let index = inscriptionsTournament.value.findIndex((a) => {
			return a.name == tournName;
		});

		if (index === -1) {
			index = inscriptionsTournament.value.length;
			inscriptionsTournament.value.push({
				name: tournName,
				athletes: [],
				id: inscription.tournament.id,
			});
		}
		inscriptionsTournament.value[index].athletes.push({
			athlete: inscription.athlete_competition,
			athlete_id: inscription.athlete_competition_id,
			payment_comprovative_url: inscription.payment_comprovative_url,
			accepted: inscription.accepted,
		});

		const atName = getAthleteNameTeam(inscription.athlete_competition);
		index = inscriptionsAthlete.value.findIndex((a) => {
			return a.id == inscription.athlete_competition_id;
		});

		if (index === -1) {
			index = inscriptionsAthlete.value.length;
			inscriptionsAthlete.value.push({
				name: atName,
				tournaments: [],
				id: inscription.athlete_competition_id,
			});
		}
		inscriptionsAthlete.value[index].tournaments.push({
			name: tournName,
			tournament_id: inscription.tournament_id,
			payment_comprovative_url: inscription.payment_comprovative_url,
			accepted: inscription.accepted,
		});
	}
	inscriptionsTournament.value.sort((a, b) => {
		if (a.name < b.name) {
			return -1;
		}
		if (a.name > b.name) {
			return 1;
		}
		return 0;
	});
};

const toogleSelectedForPaymentGuide = (athlete_id, tournament_id) => {
	const index = selectedForPaymentGuide.value.findIndex(
		(a) => a.athlete_competition_id === athlete_id && a.tournament_id === tournament_id
	);
	if (index === -1) {
		selectedForPaymentGuide.value.push({
			athlete_competition_id: athlete_id,
			tournament_id: tournament_id,
		});
	} else {
		selectedForPaymentGuide.value.splice(index, 1);
	}
};

const toogleSelectedForPaymentComprovative = (athlete_id, tournament_id) => {
	const index = selectedForPaymentComprovative.value.findIndex(
		(a) => a.athlete_competition_id === athlete_id && a.tournament_id === tournament_id
	);
	if (index === -1) {
		selectedForPaymentComprovative.value.push({
			athlete_competition_id: athlete_id,
			tournament_id: tournament_id,
		});
	} else {
		selectedForPaymentComprovative.value.splice(index, 1);
	}
};

const selectAllForPaymentGuide = () => {
	selectedForPaymentGuide.value = inscriptions.value.map((a) => ({
		athlete_competition_id: a.athlete_competition_id,
		tournament_id: a.tournament_id,
	}));
};

const selectAllForPaymentComprovative = () => {
	selectedForPaymentComprovative.value = inscriptions.value.map((a) => ({
		athlete_competition_id: a.athlete_competition_id,
		tournament_id: a.tournament_id,
	}));
};

const getPaymentGuide = async () => {
	if (selectedForPaymentGuide.value.length === 0) {
		toast.error(t("error.inscriptionPaymentGuide"));
		return;
	}
	loadingDownloadPaymentGuide.value = true;
	try {
		const { data } = await authApi.post(
			`inscriptions/get-payment-guide?team_id=${props.teamId}`,
			selectedForPaymentGuide.value,
			{ responseType: "blob" }
		);

		const pdfUrl = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = "payment_guide.pdf";
		a.href = pdfUrl;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(pdfUrl);
		}, 100);

		selectForPaymentGuide.value = false;
		selectedForPaymentGuide.value = [];
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingDownloadPaymentGuide.value = false;
	}
};

const sendPaymentComprovative = async () => {
	if (selectedForPaymentComprovative.value.length === 0) {
		toast.error(t("error.insurancePaymentGuide"));
		return;
	}
	loadingSendingPaymentComprovative.value = true;

	try {
		const formData = new FormData();
		formData.append("inscriptions", JSON.stringify(selectedForPaymentComprovative.value));
		formData.append("file", paymentComprovative.value);
		const { data } = await authApi.put(`inscriptions/payment-comprovative`, formData, {
			headers: { "Content-Type": "multipart/form-data" },
		});
		selectForPaymentComprovative.value = false;
		selectedForPaymentComprovative.value = [];
		getInscriptions();
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingSendingPaymentComprovative.value = false;
	}
};

const copyList = () => {
	function listener(e) {
		e.clipboardData.setData(
			"text/html",
			showAthleteInscriptions.value
				? copyListHtmlAthletes.value.innerHTML
				: copyListHtmlTournaments.value.innerHTML
		);
		e.preventDefault();
	}
	document.addEventListener("copy", listener);
	document.execCommand("copy"); // Deprecated but found no alternative for rich text copy
	document.removeEventListener("copy", listener);
	toast.success(t("copied"));
};

const deleteInscription = async (athlete_id, tournament_id) => {
	try {
		await authApi.delete(`inscriptions/tournaments/${tournament_id}/${athlete_id}`);
		getInscriptions();
	} catch (e) {
		errorHandling(e);
	}
};
</script>
