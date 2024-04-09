<template>
	<table class="mx-auto border border-black divide-y divide-black">
		<caption
			class="font-bold text-xl py-2 text-center border border-black border-b-0 bg-blue-500 rounded-t-xl">
			{{
				props.title
			}}
		</caption>
		<tr class="divide-x divide-black bg-blue-400">
			<th class="px-2 py-1">{{ t("place") }}</th>
			<th class="px-2 py-1">{{ t("name") }}</th>
			<th class="px-2 py-1">{{ t("points") }}</th>
		</tr>
		<tr
			v-for="(result, index) in props.results"
			:key="result.id"
			class="divide-x divide-black text-center odd:bg-white even:bg-blue-200">
			<td class="px-1 py-0.5">{{ index + 1 + ".º" }}</td>
			<td class="px-1 py-0.5">
				<router-link
					:to="getUrl({ id: result.id, competitionId: result?.competitionId })"
					target="_blank"
					class="inline-flex">
					{{ result.name }}
					<ArrowTopRightOnSquareIcon class="w-4 h-4 my-auto ml-1" />
				</router-link>
			</td>
			<td class="px-1 py-0.5">{{ result.points }}</td>
		</tr>
	</table>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ArrowTopRightOnSquareIcon } from "@heroicons/vue/24/solid";

const { t } = useI18n({ useScope: "global" });
const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	results: {
		type: Object,
		required: true,
	},
	getUrl: {
		type: Function,
		required: true,
	},
});
</script>
