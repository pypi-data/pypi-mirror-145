"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.KoreIO = void 0;
var readline_1 = __importDefault(require("readline"));
var Board_1 = require("./Board");
var KoreIO = /** @class */ (function () {
    /**
     * Constructor for a new agent
     * User should edit this according to the `Design` this agent will compete under
     */
    function KoreIO() {
        this._setup(); // DO NOT REMOVE
    }
    KoreIO.prototype._setup = function () {
        var _this = this;
        // Prepare to read input
        var rl = readline_1.default.createInterface({
            input: process.stdin,
            output: null,
        });
        var buffer = [];
        var currentResolve;
        var currentPromise;
        var makePromise = function () {
            return new Promise(function (resolve) {
                currentResolve = resolve;
            });
        };
        // on each line, push line to buffer
        rl.on('line', function (line) {
            buffer.push(line);
            currentResolve();
            currentPromise = makePromise();
        });
        // The current promise for retrieving the next line
        currentPromise = makePromise();
        // with await, we pause process until there is input
        this.getLine = function () { return __awaiter(_this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                return [2 /*return*/, new Promise(function (resolve) { return __awaiter(_this, void 0, void 0, function () {
                        return __generator(this, function (_a) {
                            switch (_a.label) {
                                case 0:
                                    if (!(buffer.length === 0)) return [3 /*break*/, 2];
                                    // pause while buffer is empty, continue if new line read
                                    return [4 /*yield*/, currentPromise];
                                case 1:
                                    // pause while buffer is empty, continue if new line read
                                    _a.sent();
                                    return [3 /*break*/, 0];
                                case 2:
                                    // once buffer is not empty, resolve the most recent line in stdin, and remove it
                                    resolve(buffer.shift());
                                    return [2 /*return*/];
                            }
                        });
                    }); })];
            });
        }); };
    };
    KoreIO.prototype.run = function (loop) {
        return __awaiter(this, void 0, void 0, function () {
            var _loop_1, this_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _loop_1 = function () {
                            var rawObservation, rawConfiguration, board, nextBoard, actions_1;
                            return __generator(this, function (_b) {
                                switch (_b.label) {
                                    case 0: return [4 /*yield*/, this_1.getLine()];
                                    case 1:
                                        rawObservation = _b.sent();
                                        return [4 /*yield*/, this_1.getLine()];
                                    case 2:
                                        rawConfiguration = _b.sent();
                                        board = Board_1.Board.fromRaw(rawObservation, rawConfiguration);
                                        try {
                                            nextBoard = loop(board);
                                            actions_1 = [];
                                            board.currentPlayer.nextActions.forEach(function (action, id) { return actions_1.push("".concat(id, ":").concat(action.toString())); });
                                            console.log(actions_1.join(","));
                                        }
                                        catch (err) {
                                            console.log(err);
                                        }
                                        return [2 /*return*/];
                                }
                            });
                        };
                        this_1 = this;
                        _a.label = 1;
                    case 1:
                        if (!true) return [3 /*break*/, 3];
                        return [5 /*yield**/, _loop_1()];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 1];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    return KoreIO;
}());
exports.KoreIO = KoreIO;
//# sourceMappingURL=KoreIO.js.map