"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * This is a lambda that subscribes to every eventbridge etl event that is sent and logs them in one place
 */
exports.handler = async (event) => {
    console.log(JSON.stringify(event, null, 2));
};