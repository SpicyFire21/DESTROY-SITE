import axios from 'axios';
import pocketbase from 'pocketbase';

const pb = new pocketbase('https://trackhuntergame.bessarion.fr');
export async function getAgent(id: string, n: number) {

    try {
        const data = await pb.collection('agents').getFullList(id, { '$autoCancel': false,});
        const request = await axios.get('https://valorant-api.com/v1/agents/' + data[n].agent_id);
        return [request.data.data.displayName, request.data.data.fullPortrait, data[n].win_ratio];
    } catch (error) {
        console.error(error);
    }
}

console.log(await getAgent('dw866jyp9qvhsjr', 0));
