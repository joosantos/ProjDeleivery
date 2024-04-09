<template>
	<div>
		<h1 class="text-3xl font-semibold text-center">
			{{ athlete == null ? t("athletesPage") : athlete.name }}
		</h1>
		<Loading v-if="loading" />
		<div v-else class="mt-4">
			<div class="inline-flex">
				<div>
					<img
						class="w-40 h-40 rounded-lg"
						:src="
							athlete.profile_picture_url
								? `https://kempo-files.fra1.digitaloceanspaces.com/${athlete.profile_picture_url}`
								: '/defaultUserImage.png'
						"
						:alt="`Profile picture for ${athlete.name}`" />
				</div>
				<div class="ml-4 text-xl">
					<p>
						{{
							athlete.birthday
								? t("athletePage.age", { age: getAge(athlete.birthday) })
								: t("athletePage.noAge")
						}}
					</p>
					<p>
						{{
							athlete.weight
								? t("athletePage.weight", { weight: athlete.weight })
								: t("athletePage.noWeight")
						}}
					</p>
					<p>
						{{
							athlete.belt
								? t("athletePage.graduation", {
										graduation: t(`belts.${athlete.belt.name}`),
								  })
								: t("athletePage.noGraduation")
						}}
					</p>
					<div class="inline-flex text-xl">
						<p>{{ t("athletePage.federated", { federated: "" }) }}</p>
						<CheckIcon
							v-if="athlete.federated_in_current_season"
							class="w-8 h-8 text-green-500 ml-1 -mt-0.5" />
						<XMarkIcon v-else class="w-8 h-8 text-red-500 ml-1 -mt-0.5" />
					</div>
				</div>
			</div>

			<!-- Year -->
			<p class="text-center text-3xl font-medium">Tournaments participated</p>
			<CustomInput
				class="max-w-max"
				:label="t('forms.season')"
				type="text"
				:name="'year'"
				:mask="'####'"
				:option-selected="year"
				sizeText="large"
				:error="''"
				@value-changed="
					(option) => {
						year = option;
						getTournaments();
					}
				" />
			<Loading v-if="loadingTournaments" />
			<div v-else class="flex flex-col gap-y-8 w-full lg:flex-row lg:gap-x-8 lg:gap-y-0 mt-2">
				<ShowTournamentAthlete :tournaments="athlete.first" :place="1" />
				<ShowTournamentAthlete :tournaments="athlete.second" :place="2" />
				<ShowTournamentAthlete :tournaments="athlete.third" :place="3" />
				<ShowTournamentAthlete :tournaments="athlete.other" :place="4" />
			</div>
		</div>
	</div>
</template>
*
<script setup>
import { unauthApi, errorHandling } from "@/services/api";
import { ref, onMounted } from "vue";
import { XMarkIcon, CheckIcon } from "@heroicons/vue/24/solid";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import ShowTournamentAthlete from "@/components/athletes/partials/showTournamentAthlete.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	athleteId: {
		type: String,
		required: true,
	},
});
const athlete = ref(null);
const loading = ref(true);
const loadingTournaments = ref(true);
const today = ref(new Date());
const year = ref(today.value.getFullYear());

onMounted(() => {
	getTournaments();
});

const getTournaments = async () => {
	if (year.value < 2021) return;
	loadingTournaments.value = true;
	try {
		const { data } = await unauthApi.get(
			`athletes/${props.athleteId}/public?year=${year.value}`
		);
		athlete.value = data;
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
		loadingTournaments.value = false;
	}
};

const getAge = (birthday) => {
	let birthDate = new Date(birthday);
	let age = today.value.getFullYear() - birthDate.getFullYear();
	let m = today.value.getMonth() - birthDate.getMonth();
	if (m < 0 || (m === 0 && today.value.getDate() < birthDate.getDate())) {
		age--;
	}
	return age;
};
</script>
