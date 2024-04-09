<template>
	<div class="mt-20 px-20 relative">
		<div
			id="border"
			:class="[
				'border-b-[24px] border-r-[24px] border-l-[24px] rounded-full relative top-10 opacity-0 transition-all duration-[2000ms]',
				props.isRed ? 'border-red-500' : 'border-blue-500',
			]">
			<p
				id="winner"
				class="text-9xl font-bold text-yellow-500 text-center uppercase"
				:style="[
					props.isRed
						? 'text-shadow: 1px 1px 2px red, 0 0 1em red, 0 0 0.2em red'
						: 'text-shadow: 1px 1px 2px blue, 0 0 1em blue, 0 0 0.2em blue',
				]">
				Winner
			</p>
			<div class="max-w-max mx-auto mt-20">
				<div
					id="name"
					:class="[
						'border-8 px-40 pb-8 pt-4 text-9xl font-semibold text-center rounded-full relative top-40 opacity-0 transition-all duration-[2000ms]',
						props.isRed ? 'border-red-500' : 'border-blue-500',
					]">
					{{ props.name }}
				</div>
				<div
					id="club"
					class="border border-gray-400 px-20 pb-2 pt-1 text-4xl mt-6 font-semibold text-center rounded-xl relative top-40 opacity-0 transition-all duration-[2000ms]">
					{{ props.team }}
				</div>
			</div>
			<div class="h-20" />
			<div class="absolute -bottom-10 left-1/2 -translate-x-1/2 bg-gray-200 w-80 h-10" />
			<div
				class="relative left-1/2 -translate-x-1/2 top-16 h-32 w-32 border-2 border-black bg-gray-200 rounded-lg">
				<p class="text-3xl text-center">Match</p>
				<p class="text-7xl text-center font-semibold">{{ props.match }}</p>
			</div>
		</div>
	</div>
</template>
<script setup>
const props = defineProps({
	isRed: {
		type: Boolean,
		required: true,
	},
	name: {
		type: String,
		required: true,
	},
	match: {
		type: Number,
		required: true,
	},
	team: {
		type: String,
		required: false,
		default: " ",
	},
});

setTimeout(function () {
	document.getElementById("border").classList.remove("top-10");
	document.getElementById("border").classList.remove("opacity-0");
	document.getElementById("border").classList.add("top-0");
	setTimeout(function () {
		document.getElementById("name").classList.remove("top-40");
		document.getElementById("name").classList.remove("opacity-0");
		document.getElementById("name").classList.add("top-0");
		document.getElementById("club").classList.remove("top-40");
		document.getElementById("club").classList.remove("opacity-0");
		document.getElementById("club").classList.add("top-0");
	}, 500);
}, 250);
</script>
