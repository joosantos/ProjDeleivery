<template>
	<button
		type="button"
		:class="[
			'cursor-pointer group relative w-full border-gray-300 border-dashed rounded-lg text-center hover:border-gray-400',
			props.size == 'M'
				? 'p-12 border-2'
				: props.size == 'S'
				? 'p-4 border'
				: 'p-24 border-4',
		]"
		@click="emit('create')">
		<div :class="['mx-auto', props.size == 'S' ? 'inline-flex' : 'block']">
			<component
				:is="props.comp"
				:class="[
					'text-gray-400 group-hover:text-gray-600',
					props.size == 'M'
						? 'h-12 w-12 mx-auto'
						: props.size == 'S'
						? 'h-6 w-6'
						: 'h-24 w-24 mx-auto',
				]" />
			<span
				:class="[
					'block text-sm font-medium text-gray-900 group-hover:text-black',
					props.size == 'S' ? 'mt-0.5 ml-2' : 'mt-2',
					props.size == 'L' ? 'text-xl' : '',
				]">
				{{ props.objectType }}
			</span>
		</div>
	</button>
</template>

<script setup>
const props = defineProps({
	objectType: {
		type: String,
		required: true,
	},
	comp: {
		type: Function,
		required: true,
	},
	size: {
		type: String,
		required: false,
		default: "M",
		validator(value) {
			// The value must match one of these strings
			return ["S", "M", "L"].includes(value);
		},
	},
});

const emit = defineEmits(["create"]);
</script>
