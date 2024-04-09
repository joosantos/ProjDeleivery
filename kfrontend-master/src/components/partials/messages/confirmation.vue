<template>
	<Modal :open="props.open" @close="emit('close')">
		<div class="bg-white">
			<div class="px-4 py-5 sm:p-6">
				<h3 class="text-lg leading-6 font-medium text-gray-900">
					{{ props.title }}
				</h3>
				<div class="mt-2 max-w-xl text-sm text-gray-500">
					<p>
						{{ props.message }}
					</p>
				</div>
				<div class="mt-5 inline-flex max-h-min">
					<button
						type="button"
						class="cursor-pointer mr-2 bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
						@click="emit('close')">
						{{ t("back") }}
					</button>
					<button
						type="button"
						:class="[
							'inline-flex px-4 py-2 border border-transparent font-medium rounded-md   hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2  sm:text-sm relative',
							props.isDelete
								? 'text-red-700 bg-red-100 focus:ring-red-500'
								: 'text-blue-700 bg-blue-100 focus:ring-blue-500',
						]"
						@click="props.isDelete ? emit('deleted') : emit('confirmed')">
						<div class="left-1/2 absolute -translate-x-1/2">
							<svg
								v-if="props.loading"
								class="animate-spin h-5 w-5"
								viewBox="0 0 50 50">
								<path
									fill="currentColor"
									d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z"></path>
							</svg>
						</div>
						<p :class="[props.loading ? 'opacity-0 relative' : '']">
							{{ props.buttonText }}
						</p>
					</button>
				</div>
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	message: {
		type: String,
		required: true,
	},
	buttonText: {
		type: String,
		required: true,
	},
	open: {
		type: Boolean,
		required: true,
	},
	loading: {
		required: false,
		default: false,
		type: Boolean,
	},
	showX: {
		required: false,
		default: false,
		type: Boolean,
	},
	isDelete: {
		required: false,
		default: true,
		type: Boolean,
	},
});
const emit = defineEmits(["close", "deleted", "confirmed"]);
</script>
