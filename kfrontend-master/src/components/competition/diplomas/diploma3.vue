<template>
	<img v-show="false" id="img" src="/diploma3.jpg" />
	<canvas id="canvas"></canvas>
	<canvas v-show="false" id="canvasText"></canvas>
</template>

<script setup>
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";
import { getAthleteName, getTeamName } from "@/services/athlete.service.js";

let { t } = useI18n();

const props = defineProps({
	// ID of the tournament
	tournament: {
		type: String,
		required: true,
	},
});

authApi
	.get(`tournaments/${props.tournament}`)
	.then((response) => {
		let name = getAthleteName(response.data.third_place);
		let team = getTeamName(response.data.third_place);
		let canvas = document.getElementById("canvas");
		let ctx = canvas.getContext("2d");
		let img = document.getElementById("img");
		canvas.width = img.width;
		canvas.height = img.height;
		canvas.crossOrigin = "Annonymous";
		ctx.drawImage(img, 0, 0);
		ctx.font = team ? "30pt Verdana" : "60pt Verdana";
		let extraTop = 20;

		let canvasText = document.getElementById("canvas");
		let context = canvasText.getContext("2d");
		context.font = ctx.font;
		let nameWidth = 0;
		for (let n of name.split(",")) {
			let aux = context.measureText(n).width;
			if (aux > nameWidth) {
				nameWidth = aux;
			}
		}

		if (nameWidth > 880) {
			extraTop = 10;
			ctx.font = "50pt Verdana";
			context.font = ctx.font;
			nameWidth = 0;
			for (let n of name.split(",")) {
				let aux = context.measureText(n).width;
				if (aux > nameWidth) {
					nameWidth = aux;
				}
			}
		}

		if (nameWidth > 880) {
			extraTop = 0;
			ctx.font = "40pt Verdana";
			context.font = ctx.font;
			nameWidth = 0;
			for (let n of name.split(",")) {
				let aux = context.measureText(n).width;
				if (aux > nameWidth) {
					nameWidth = aux;
				}
			}
		}

		if (nameWidth > 880) {
			extraTop = 0;
			ctx.font = "30pt Verdana";
			context.font = ctx.font;
			nameWidth = 0;
			for (let n of name.split(",")) {
				let aux = context.measureText(n).width;
				if (aux > nameWidth) {
					nameWidth = aux;
				}
			}
		}
		let leftSide = 0;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.drawImage(img, 0, 0);
		ctx.fillStyle = "black";

		let i = -50;
		for (let n of name.split(",")) {
			if (team && i != 50) {
				n = n + ",";
			}
			nameWidth = context.measureText(n).width;
			leftSide = (890 - nameWidth) / 2;
			ctx.fillText(n, 360 + leftSide, 460 + (team ? i : extraTop));
			i += 50;
		}

		ctx.font = "20pt Verdana";
		let category = response.data.category.name;
		context.font = ctx.font;
		nameWidth = context.measureText(category).width;

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "17.5pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "15pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "14pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "13pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "12pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "11pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		if (nameWidth > 380) {
			extraTop = 0;
			ctx.font = "10pt Verdana";
			context.font = ctx.font;
			nameWidth = context.measureText(category).width;
		}

		leftSide = (380 - nameWidth) / 2;
		ctx.font = "20pt Verdana";
		ctx.fillStyle = "black";
		ctx.fillText(category, 460 + leftSide, 690);
		context.font = ctx.font;
		nameWidth = context.measureText(category).width;

		//refill text
		let age = "";
		if (response.data.age_min == null) {
			if (response.data.age_max != null) {
				age = "-" + response.data.age_max;
			}
		} else {
			if (response.data.age_max == null) {
				age = "+" + response.data.age_max;
			} else {
				age = response.data.age_min + "/" + response.data.age_max;
			}
		}
		if (age != "") {
			context.font = ctx.font;
			nameWidth = context.measureText(age).width;

			leftSide = (100 - nameWidth) / 2;
			ctx.fillStyle = "black";
			ctx.fillText(age, 1070 + leftSide, 690);
		}

		let weight = "";
		if (response.data.weight_min == null) {
			if (response.data.weight_max != null) {
				weight = "-" + response.data.weight_max + "Kg.";
			}
		} else {
			if (response.data.weight_max == null) {
				weight = "+" + response.data.weight_max + "Kg.";
			} else {
				weight = response.data.weight_min + "Kg./" + response.data.weight_max + "Kg.";
			}
		}
		if (weight != "") {
			context.font = ctx.font;
			nameWidth = context.measureText(weight).width;

			leftSide = (340 - nameWidth) / 2;
			ctx.fillStyle = "black";
			ctx.fillText(weight, 530 + leftSide, 731);
		}
	})
	.catch(() => {
		toast.error(t("notLoaded"));
	});
</script>

<i18n>
{
	"en_GB": {
		"notLoaded": "It wasn't possible to load the athlete"
	},
	"pt_PT": {
		"notLoaded": "Não foi possível carregar o atleta"
	}
}
</i18n>
