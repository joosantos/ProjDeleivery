<template>
	<div>
		<TransitionRoot as="template" :show="props.open">
			<Dialog
				as="div"
				class="fixed z-20 inset-0 overflow-y-auto"
				@close="props.outsideClick && emit('close')">
				<div
					class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0"
						enter-to="opacity-100"
						leave="ease-in duration-200"
						leave-from="opacity-100"
						leave-to="opacity-0">
						<DialogOverlay
							class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
					</TransitionChild>

					<!-- This element is to trick the browser into centering the modal contents. -->
					<span
						class="hidden sm:inline-block sm:align-middle sm:h-screen"
						aria-hidden="true">
						&#8203;
					</span>
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enter-to="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in duration-200"
						leave-from="opacity-100 translate-y-0 sm:scale-100"
						leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
						<div
							:class="[
								'inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-visible shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full sm:p-6',
								`sm:max-w-${size}`,
							]">
							<XCircleIcon
								v-if="props.showX || !props.outsideClick"
								class="w-10 h-10 text-gray-600 absolute top-4 right-6 hover:text-gray-900 cursor-pointer"
								@click="emit('close')" />
							<div v-if="props.showX || !props.outsideClick" class="mt-10"></div>
							<slot></slot>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
		<div class="max-w-xl hidden" />
		<div class="max-w-2xl hidden" />
		<div class="max-w-3xl hidden" />
		<div class="max-w-4xl hidden" />
		<div class="max-w-5xl hidden" />
		<div class="max-w-6xl hidden" />
		<div class="max-w-7xl hidden" />
	</div>
</template>

<script setup>
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { XCircleIcon } from "@heroicons/vue/24/outline";

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	showX: {
		type: Boolean,
		required: false,
		default: false,
	},
	outsideClick: {
		type: Boolean,
		required: false,
		default: true,
	},
	size: {
		type: String,
		required: false,
		default: "3xl ",
	},
});
const emit = defineEmits(["close"]);
</script>
