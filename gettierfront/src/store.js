import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'
import VueNativeSock from 'vue-native-websocket'
Vue.use(Vuex)
const store = new Vuex.Store({
    state: {
        id_in_group: window.id_in_group,
        messages: [],
        socket: {
            isConnected: false,
            message: '',
            reconnectError: false,
        },
        chatEndModal: false,
        saving: false,
        djangoErrors: window.djangoErrors,
        errorDialog: _.isEmpty(window.djangoErrors) !== true,
        chatExitAllowed: false,
        chatExitForced: false,
        instructionsShow: false,
    },
    getters: {
        status: (state) => state.socket.isConnected,
        savingStatus: (state) => state.saving,
    },
    mutations: {
        setEndChatModel:(state, value)=> {
            state.chatEndModal=value
        },
        toggleChatEndModal:state=>(state.chatEndModal=!state.chatEndModal),
        allowExitPermission: (state) => (state.chatExitAllowed = true),
        forceExit: (state) => (state.chatExitForced = true),
        toggleErrorDialog: (state) => (state.errorDialog = !state.errorDialog),
        toggleInstructionsDialog: (state) => (state.instructionsShow = !state.instructionsShow),
        SAVING_INITIATED(state) {
            state.saving = true
        },
        SAVING_DONE(state) {
            state.saving = false
        },
        addMessage(state, message) {
            const { owner } = message;
            const lastone = state.messages[state.messages.length - 1]
            if (lastone) {
                const { subgroup: prevsubgroup, owner: prevowner } = lastone;
                if (owner === prevowner) {
                    message.subgroup = prevsubgroup;
                    lastone.last = false;
                    message.last = true;

                } else {
                    message.subgroup = prevsubgroup + 1;
                    lastone.last = true;
                    message.first = true;
                    message.last = true;
                }
            }
            else {
                message.subgroup = 0;
                message.first = true;
                message.last = true;

            }
            state.messages.push(message)
        },
        SOCKET_ONOPEN(state, event) {
            Vue.prototype.$socket = event.currentTarget
            state.socket.isConnected = true
        },
        SOCKET_ONCLOSE(state, event) {
            state.socket.isConnected = false
        },
        SOCKET_ONERROR(state, event) {
            console.error(state, event)
        },
        // default handler called for all methods
        SOCKET_ONMESSAGE(state, message) {
           
        },
        // mutations for reconnect methods
        SOCKET_RECONNECT(state, count) {
            console.info(state, count)
        },
        SOCKET_RECONNECT_ERROR(state) {
            state.socket.reconnectError = true;
        },
    },
    actions: {
        sendMessage: function (context, message) {
            context.commit('addMessage', message);
            Vue.prototype.$socket.sendObj(message)
        },
        incomingMessage: function (context, message) {
            console.debug('INCOMING messagei incoming', message);
            context.commit('addMessage', message);
        },
        endOfChat: function(context, message){
            context.commit('setEndChatModel', {value: true})
            
        },
        confirm: function (context, message) {
            console.debug('messagei confirmed', message)
        },

        requestOldMessages: function (context) {
            const message = { request_old_messages: true }
            Vue.prototype.$socket.sendObj(message)
        },
        sendDecision: function (context, decision) {
            const message = { decision: decision }
            Vue.prototype.$socket.sendObj(message)
        },
        PrevMessages: function (context, message) {
            console.debug('previous messages received');
            const { msgs, chatStatus } = message
            if (chatStatus === false) {
                context.commit('forceExit');
            }
            if (msgs) {
                msgs.forEach(m => {
                    console.debug(m);
                    context.commit('addMessage', m);
                });

            }
        },
        savingRequested: function ({ commit }
        ) {
            console.debug('saving request initiated');
            commit('SAVING_INITIATED')
        },
        savingStopRequested: function ({ commit }
        ) {
            console.debug('saving STOP request initiated');
            commit('SAVING_DONE')
        }

    }
})
const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
const ws_path = ws_scheme + '://' + window.location.host + window.socket_path;
Vue.use(VueNativeSock, ws_path, {
    store: store,
    format: 'json',
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000,
});
export default store;  