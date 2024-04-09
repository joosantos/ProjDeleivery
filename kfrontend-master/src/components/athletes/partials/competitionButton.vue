<script setup>
const props = defineProps({
	name: {
		type: String,
		required: true,
	},
	selected: {
		type: Boolean,
		required: true,
	},
});
const emit = defineEmits(["click"]);
</script>

<template>
	<div
		:class="[
			'rounded-md border-2 py-1.5 px-3 text-lg cursor-pointer',
			props.selected
				? 'border-blue-500 bg-blue-100'
				: 'border-gray-500 bg-gray-100 opacity-50 hover:opacity-100',
		]"
		@click="emit('click')">
		{{ props.name }}
	</div>
</template>
