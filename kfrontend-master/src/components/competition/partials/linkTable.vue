<template>
	<router-link
		class="inline-flex justify-between w-full cursor-pointer border relative rounded-xl px-4 py-1 group border-blue-500 hover:bg-blue-200 hover:border-blue-700 hover:-translate-y-0.5 min-w-max"
		:to="props.routerTo"
		:target="props.target">
		<p
			class="text-center w-full mt-0.5 text-blue-500 group-hover:text-blue-800 cursor-pointer select-none">
			{{ props.text }}
		</p>
	</router-link>
</template>
<script setup>
const props = defineProps({
	// Route to go
	routerTo: {
		type: Object,
		required: true,
	},
	// Text of the Button
	text: {
		type: String,
		required: true,
	},
	// Link Target
	target: {
		type: String,
		required: false,
		default: "_self",
		validator: function (value) {
			// target must be:
			return ["_blank", "_self", "_parent", "_top"].indexOf(value) != -1;
		},
	},
});
</script>
