<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<div class="max-w-max">
			<p>{{ props.label }}</p>
			<div>
				<img
					:src="newImg || props.originalImage || props.urlDefaultImage"
					class="max-w-xs"
					alt="User profile picture" />
			</div>
			<div class="mx-auto max-w-max">
				<FileInput
					:name="props.name"
					:label="''"
					:error="props.error"
					:id="props.id"
					:readonly="props.readonly"
					:disabled="props.disabled"
					:borderBlack="props.borderBlack"
					:labelBlack="props.labelBlack"
					:sizeText="props.sizeText"
					accept-types="image/jpg, image/jpeg, image/png, image/gif"
					@value-changed="updateImage" />
			</div>
		</div>
		<Modal :open="isShowModal" :outsideClick="false" @close="isShowModal = false" :size="'5xl'">
			<div class="w-full inline-flex space-x-4 ml-auto">
				<p class="text-xl font-medium w-full">{{ t("pictureCropping") }}</p>
				<Button
					class="max-w-max px-4"
					:message="t('cancel')"
					:type="'primary'"
					:pill="true"
					:size="'small'"
					@button-click="cancel" />
				<Button
					class="max-w-max px-4"
					:message="t('clear')"
					:type="'primary'"
					:pill="true"
					:size="'small'"
					@button-click="clear" />
				<Button
					class="max-w-max px-4"
					:message="t('reset')"
					:type="'primary'"
					:pill="true"
					:size="'small'"
					@button-click="reset" />
				<Button
					class="max-w-max px-4"
					:message="t('crop')"
					:type="'success'"
					:pill="true"
					:size="'small'"
					@button-click="finish" />
			</div>
			<div class="mt-4">
				<VuePictureCropper
					v-if="img"
					:boxStyle="{
						width: '100%',
						height: '100%',
						backgroundColor: '#f8f8f8',
						margin: 'auto',
					}"
					:img="img"
					:options="{
						viewMode: 1,
						dragMode: 'crop',
						aspectRatio: 1 / 1,
					}"
					@ready="null" />
			</div>
		</Modal>
	</div>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import Button from "@/components/partials/button.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import VuePictureCropper, { cropper } from "vue-picture-cropper";
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { ref, reactive } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	// Name of the input for internal reference
	name: {
		type: String,
		required: true,
	},
	// Label of the input to be displayed
	label: {
		type: String,
		required: true,
	},
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
	// ID of the input for internal reference
	id: {
		type: String,
		required: false,
		default: null,
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
	disabled: {
		type: Boolean,
		required: false,
		default: false,
	},
	borderBlack: {
		type: Boolean,
		required: false,
		default: false,
	},
	labelBlack: {
		type: Boolean,
		required: false,
		default: false,
	},
	originalImage: {
		type: String,
		required: false,
		default: "",
	},
	urlDefaultImage: {
		type: String,
		required: false,
		default: "/noImageFound.jpg",
	},
	sizeText: {
		type: String,
		required: false,
		default: "medium",
		validator(value) {
			// The sizeText must match one of these strings
			return ["small", "medium", "large"].includes(value);
		},
	},
});

const img = ref("");
const isShowModal = ref(false);
const result = reactive({
	dataURL: "",
	blobURL: "",
});
const newImg = ref(null);
const uploadInput = ref(null);

const emit = defineEmits(["valueChanged"]);
const updateImage = (file) => {
	// Reset last selection and results
	img.value = "";
	result.dataURL = "";
	result.blobURL = "";

	// Convert to dataURL and pass to the cropper component
	const reader = new FileReader();
	reader.readAsDataURL(file);
	reader.onload = () => {
		// Update the picture source of the `img` prop
		img.value = String(reader.result);

		// Show the modal
		isShowModal.value = true;

		// Clear selected files of input element
		if (!uploadInput.value) return;
		uploadInput.value.value = "";
	};
};
const cancel = () => {
	isShowModal.value = false;
};
const clear = () => {
	if (!cropper) return;
	cropper.clear();
};
const reset = () => {
	if (!cropper) return;
	cropper.reset();
};
const finish = async () => {
	if (!cropper) return;
	const base64 = cropper.getDataURL();
	const blob = await cropper.getBlob();
	if (!blob) return;

	const file = await cropper.getFile({
		fileName: "userProfile",
	});

	result.dataURL = base64;
	result.blobURL = URL.createObjectURL(blob);
	newImg.value = result.dataURL;
	isShowModal.value = false;
	emit("valueChanged", file);
};
</script>
