import { browser } from "$app/env";

let baseUrl = 'https://api.eyo.kr:8081';
if (browser) {
	baseUrl = 'https://api.eyo.kr:8081';
}

export default { baseUrl };