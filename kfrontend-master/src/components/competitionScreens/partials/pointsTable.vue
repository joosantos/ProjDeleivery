<template>
	<div v-if="tournamentExists" class="bg-red-600 p-2 rounded-xl border border-black">
		<p class="text-center capitalize font-medium text-xl">{{ t("pontuation") }}</p>
		<table class="table-auto border-collapse">
			<thead>
				<tr>
					<th></th>
					<th class="text-center capitalize">
						{{ t("judge", { number: 1 }) }}
					</th>
					<th class="text-center capitalize">
						{{ t("central") }}
					</th>
					<th class="text-center capitalize">
						{{ t("judge", { number: 2 }) }}
					</th>
					<th class="text-center capitalize">
						{{ t("total") }}
					</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<th class="text-center capitalize">
						<p class="min-w-max px-1">
							{{ t("round", { number: 1 }) }}
						</p>
					</th>
					<td class="text-center capitalize">
						<PointsInput
							:points="points.judge1.round1"
							@update-points="(option) => (points.judge1.round1 = option)" />
					</td>
					<td class="text-center capitalize">
						<PointsInput
							:points="points.central.round1"
							@update-points="(option) => (points.central.round1 = option)" />
					</td>
					<td class="text-center capitalize">
						<PointsInput
							:points="points.judge2.round1"
							@update-points="(option) => (points.judge2.round1 = option)" />
					</td>
					<td class="text-center capitalize">0</td>
				</tr>
			</tbody>
		</table>
		<div class="mx-auto inline-flex gap-x-2 w-full justify-center">
			<div class="max-w-min">
				<Button
					:message="t('save')"
					:type="'primary'"
					:size="'small'"
					:pill="false"
					:outline="false"
					@button-click="openModal = true" />
			</div>
			<div class="max-w-min">
				<Button
					:message="t('save')"
					:type="'primary'"
					:size="'small'"
					:pill="false"
					:outline="false"
					@button-click="openModal = true" />
			</div>
		</div>
	</div>
</template>

<script setup>
import PointsInput from "@/components/competitionScreens/partials/pointsInput.vue";
import Button from "@/components/partials/button.vue";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

let points = ref({
	judge1: {
		round1: 0,
		round2: 0,
	},
	central: {
		round1: 0,
		round2: 0,
	},
	judge2: {
		round1: 0,
		round2: 0,
	},
});

const props = defineProps({
	tournament: {
		type: Object,
		required: true,
	},
});
const tournamentExists = computed(() => {
	return !!Object.keys(props.tournament).length;
});
</script>
