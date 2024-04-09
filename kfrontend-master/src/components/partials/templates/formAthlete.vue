<template>
	<form :id="props.id" class="scroll-mt-44" @submit.prevent="emit('submited')">
		<div class="shadow sm:overflow-hidden sm:rounded-md">
			<div class="space-y-6 bg-white py-6 px-4 sm:p-6">
				<div>
					<h3 class="text-lg font-medium leading-6 text-gray-900">
						{{ props.title }}
					</h3>
					<p class="mt-1 text-sm text-gray-500">
						{{ props.subtitle }}
					</p>
				</div>
				<div class="grid grid-cols-12 gap-6">
					<slot></slot>
				</div>
			</div>
			<div class="bg-gray-50 px-4 py-3 text-right sm:px-6">
				<button
					v-if="props.canEdit && props.showButton"
					type="submit"
					class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
					<svg
						v-if="props.showLoading"
						class="animate-spin w-6 h-6 mx-auto"
						viewBox="0 0 50 50">
						<path
							fill="currentColor"
							d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z"></path>
					</svg>
					<div v-else class="inline-flex relative">
						<p class="text-sm">
							{{ props.buttonSave }}
						</p>

						<XCircleIcon
							v-show="props.showX"
							style="width: 22px"
							class="relative ml-3 top-1/2 -translate-y-1/2"></XCircleIcon>
					</div>
				</button>
				<button
					v-else-if="props.showButton"
					type="button"
					class="inline-flex justify-center rounded-md border border-transparent bg-yellow-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2"
					@click.prevent="emit('edit')">
					<svg
						v-if="props.showLoading"
						class="animate-spin w-6 h-6 mx-auto"
						viewBox="0 0 50 50">
						<path
							fill="currentColor"
							d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z"></path>
					</svg>
					<div v-else class="inline-flex relative">
						<p class="text-sm">
							{{ props.buttonEdit }}
						</p>

						<XCircleIcon
							v-show="props.showX"
							style="width: 22px"
							class="relative ml-3 top-1/2 -translate-y-1/2"></XCircleIcon>
					</div>
				</button>
			</div>
		</div>
	</form>
</template>
<script setup>
import { XCircleIcon } from "@heroicons/vue/24/outline";
const props = defineProps({
	id: {
		type: String,
		required: true,
	},
	title: {
		type: String,
		required: true,
	},
	subtitle: {
		type: String,
		required: true,
	},
	buttonSave: {
		type: String,
		required: true,
	},
	buttonEdit: {
		type: String,
		required: true,
	},
	canEdit: {
		type: Boolean,
		required: true,
	},
	showLoading: {
		type: Boolean,
		required: false,
		default: false,
	},
	showX: {
		type: Boolean,
		required: false,
		default: false,
	},
	showButton: {
		type: Boolean,
		required: false,
		default: true,
	},
});
const emit = defineEmits(["submited", "edit"]);
</script>
