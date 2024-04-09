<template>
	<button
		type="button"
		class="inline-flex bg-gray-200 max-w-max cursor-pointer pl-2 py-0.5 rounded-lg border border-gray-300 group hover:bg-gray-300 hover:shadow-sm hover:border-gray-500"
		@click.prevent="emit('buttonClick')">
		<p class="min-w-max my-auto">{{ props.text }}</p>
		<TrashIcon class="h-8 w-8 py-1 text-gray-500 my-auto group-hover:text-gray-700" />
	</button>
</template>
<script setup>
import { TrashIcon } from "@heroicons/vue/24/solid";

const props = defineProps({
	text: {
		type: String,
		required: true,
	},
});

const emit = defineEmits(["buttonClick"]);
</script>
