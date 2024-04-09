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
			'rounded-md border-2 py-0.5 px-1.5 cursor-pointer',
			props.selected
				? 'border-blue-500 bg-blue-100'
				: 'border-gray-500 bg-gray-100 opacity-50 hover:opacity-100',
		]"
		@click="emit('click')">
		{{ props.name }}
	</div>
</template>
