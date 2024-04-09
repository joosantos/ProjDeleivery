<template>
	<div class="z-50 absolute inset-0 bg-white">
		<div class="py-2 px-4">
			<div
				class="w-full text-center border-2 border-black text-3xl font-bold p-4 rounded-full bg-gray-200">
				{{ props.title }}
			</div>
		</div>
		<div class="mt-20 px-20 relative">
			<div
				:class="[
					'border-b-[24px] border-r-[24px] border-l-[24px] rounded-full',
					props.winnerRed ? 'border-red-500' : 'border-blue-500',
				]">
				<p
					class="text-9xl font-bold text-yellow-500 text-center uppercase stroke-black"
					:style="[
						props.winnerRed
							? 'text-shadow: 1px 1px 2px red, 0 0 1em red, 0 0 0.2em red'
							: 'text-shadow: 1px 1px 2px blue, 0 0 1em blue, 0 0 0.2em blue',
					]">
					{{ t("winner") }}
				</p>
				<div class="max-w-max mx-auto mt-20">
					<div
						:class="[
							'border-8 px-40 pb-8 pt-4 text-9xl font-semibold text-center rounded-full p-4',
							props.winnerRed ? 'border-red-500' : 'border-blue-500',
						]">
						{{ props.athleteName }}
					</div>
					<div
						class="border border-gray-400 px-20 pb-2 pt-1 text-4xl mt-6 font-semibold text-center rounded-xl">
						{{ props.teamName }}
					</div>
				</div>
				<div class="h-20" />
				<div class="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-white w-80 h-10" />
				<div
					class="relative left-1/2 -translate-x-1/2 top-16 h-32 w-32 border-2 border-black bg-gray-50 rounded-lg">
					<p class="text-3xl text-center">{{ t("matchNum") }}</p>
					<p class="text-7xl text-center font-semibold">{{ props.matchNumber }}</p>
				</div>
			</div>
			<div
				class="absolute -bottom-24 left-1/2 -translate-x-1/2 text-xl border-black border-2 rounded-lg p-2 cursor-pointer hover:bg-gray-200"
				@click="emit('close')">
				{{ t("exitWinScreen") }}
			</div>
		</div>
	</div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["close"]);

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	winnerRed: {
		type: Boolean,
		required: true,
	},
	athleteName: {
		type: String,
		required: true,
	},
	teamName: {
		type: String,
		required: true,
	},
	matchNumber: {
		type: Number,
		required: true,
	},
});
</script>
