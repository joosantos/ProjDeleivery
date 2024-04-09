// tailwind.config.js
module.exports = {
	content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				primary: {
					50: "#f0ecff",
					100: "#e1d9ff",
					200: "#c4b4ff",
					300: "#a78eff",
					400: "#6D44FF",
					500: "#623de5",
					600: "#5736cc",
					700: "#412899",
					800: "#36227f",
					900: "#2b1b66",
					DEFAULT: "#6D44FF",
				},
			},
			fontFamily: {
				jost: ["'Jost'", "sans-serif"],
				morganite: ["'Morganite'", "sans-serif"],
			},
			gridTemplateRows: {
				7: "repeat(7, minmax(0, 1fr))",
				8: "repeat(8, minmax(0, 1fr))",
				9: "repeat(9, minmax(0, 1fr))",
				10: "repeat(10, minmax(0, 1fr))",
				11: "repeat(11, minmax(0, 1fr))",
				12: "repeat(12, minmax(0, 1fr))",
			},
		},
	},
	variants: {
		extend: {
			backgroundColor: ["active"],
			textColor: ["active", "visited"],
			borderColor: ["active"],
		},
	},
	plugins: [
		require("@tailwindcss/aspect-ratio"),
		require("@tailwindcss/forms"),
		require("@tailwindcss/line-clamp"),
	],
};
