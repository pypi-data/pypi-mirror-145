"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Board = void 0;
var Cell_1 = require("./Cell");
var Configuration_1 = require("./Configuration");
var Direction_1 = require("./Direction");
var Fleet_1 = require("./Fleet");
var Observation_1 = require("./Observation");
var Pair_1 = require("./Pair");
var Player_1 = require("./Player");
var Point_1 = require("./Point");
var Shipyard_1 = require("./Shipyard");
var ShipyardAction_1 = require("./ShipyardAction");
var Board = /** @class */ (function () {
    function Board(shipyards, fleets, players, currentPlayerId, configuration, step, remainingOverageTime, cells, size) {
        var _this = this;
        this.shipyards = new Map();
        shipyards.forEach(function (shipyard, shipyardId) { return _this.shipyards.set(shipyardId, shipyard.cloneToBoard(_this)); });
        this.fleets = new Map();
        fleets.forEach(function (fleet, fleetId) { return _this.fleets.set(fleetId, fleet.cloneToBoard(_this)); });
        this.players = players.map(function (player) { return player.cloneToBoard(_this); });
        this.currentPlayerId = currentPlayerId;
        this.configuration = configuration;
        this.step = step;
        this.remainingOverageTime = remainingOverageTime;
        this.cells = cells.map(function (cell) { return cell.cloneToBoard(_this); });
        this.size = size;
    }
    Board.prototype.cloneBoard = function () {
        return new Board(this.shipyards, this.fleets, this.players, this.currentPlayerId, this.configuration, this.step, this.remainingOverageTime, this.cells, this.size);
    };
    /**
     * Creates a board from the provided observation, configuration, and nextActions as specified by
     *  https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kore/kore.json
     *  Board tracks players (by id), fleets (by id), shipyards (by id), and cells (by position).
     *  Each entity contains both key values (e.g. fleet.player_id) as well as entity references (e.g. fleet.player).
     *  References are deep and chainable e.g.
     *      [fleet.kore for player in board.players for fleet in player.fleets]
     *      fleet.player.shipyards()[0].cell.north.east.fleet
     *  Consumers should not set or modify any attributes except and Shipyard.nextAction
     */
    Board.fromRaw = function (rawObservation, rawConfiguration) {
        var observation = new Observation_1.Observation(rawObservation);
        var step = observation.step;
        var remainingOverageTime = observation.remainingOverageTime;
        var configuration = new Configuration_1.Configuration(rawConfiguration);
        var currentPlayerId = observation.player;
        var players = new Array(observation.playerHlt.length);
        var fleets = new Map();
        var shipyards = new Map();
        var cells = new Array(observation.kore.length);
        var size = configuration.size;
        var board = new Board(shipyards, fleets, players, currentPlayerId, configuration, step, remainingOverageTime, cells, size);
        // Create a cell for every point in a size x size grid
        for (var x = 0; x < size; x++) {
            for (var y = 0; y < size; y++) {
                var position = new Point_1.Point(x, y);
                var kore = observation.kore[position.toIndex(size)];
                // We'll populate the cell's fleets and shipyards in _add_fleet and addShipyard
                board.cells[position.toIndex(size)] = new Cell_1.Cell(position, kore, "", "", board);
            }
        }
        var _loop_1 = function (playerId) {
            var playerKore = observation.playerHlt[playerId];
            var playerShipyards = observation.playerShipyards[playerId];
            var playerFleets = observation.playerFleets[playerId];
            board.players[playerId] = new Player_1.Player(playerId, playerKore, [], [], board);
            //player_actions = nextActions[player_id] or {}
            playerFleets.forEach(function (fleetStrs, fleetId) {
                var fleetPosIdx = parseInt(fleetStrs[0]);
                var fleetKore = parseFloat(fleetStrs[1]);
                var shipCount = parseInt(fleetStrs[2]);
                var directionIdx = parseInt(fleetStrs[3]);
                var flightPlan = fleetStrs[4];
                var fleetPosition = Point_1.Point.fromIndex(fleetPosIdx, size);
                var fleetDirection = Direction_1.Direction.fromIndex(directionIdx);
                board.addFleet(new Fleet_1.Fleet(fleetId, shipCount, fleetDirection, fleetPosition, fleetKore, flightPlan, playerId, board));
            });
            playerShipyards.forEach(function (shipyardInts, shipyardId) {
                var shipyardPosIdx = shipyardInts[0];
                var shipCount = shipyardInts[1];
                var turnsControlled = shipyardInts[2];
                var shipyardPosition = Point_1.Point.fromIndex(shipyardPosIdx, size);
                board.addShipyard(new Shipyard_1.Shipyard(shipyardId, shipCount, shipyardPosition, playerId, turnsControlled, board, undefined));
            });
        };
        for (var playerId = 0; playerId < observation.playerHlt.length; playerId++) {
            _loop_1(playerId);
        }
        return board;
    };
    Board.prototype.getCellAtPosition = function (position) {
        return this.cells[position.toIndex(this.size)];
    };
    Board.prototype.addFleet = function (fleet) {
        fleet.player.fleetIds.push(fleet.id);
        fleet.cell.fleetId = fleet.id;
        this.fleets.set(fleet.id, fleet);
    };
    Board.prototype.addShipyard = function (shipyard) {
        shipyard.player.shipyardIds.push(shipyard.id);
        shipyard.cell.shipyardId = shipyard.id;
        shipyard.cell.kore = 0;
        this.shipyards.set(shipyard.id, shipyard);
    };
    Board.prototype.deleteFleet = function (fleet) {
        var fleetIds = fleet.player.fleetIds;
        fleetIds.splice(fleetIds.indexOf(fleet.id), 1);
        if (fleet.cell.fleetId == fleet.id) {
            fleet.cell.fleetId = "";
        }
        this.fleets.delete(fleet.id);
    };
    Board.prototype.deleteShipyard = function (shipyard) {
        var shipyardsIds = shipyard.player.shipyardIds;
        shipyardsIds.splice(shipyardsIds.indexOf(shipyard.id), 1);
        if (shipyard.cell.shipyardId == shipyard.id) {
            shipyard.cell.shipyardId = "";
        }
        this.shipyards.delete(shipyard.id);
    };
    Board.prototype.getFleetAtPoint = function (position) {
        var matches = Array.from(this.fleets.values()).filter(function (fleet) { return fleet.position.equals(position); });
        return matches.length > 0 ? matches[0] : undefined;
    };
    Board.prototype.getShipyardAtPoint = function (position) {
        var matches = Array.from(this.shipyards.values()).filter(function (shipyard) { return shipyard.position.equals(position); });
        return matches.length > 0 ? matches[0] : undefined;
    };
    Object.defineProperty(Board.prototype, "currentPlayer", {
        /**
         * Returns the current player (generally this is you).
         * @return
         */
        get: function () {
            return this.players[this.currentPlayerId];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Board.prototype, "opponents", {
        /**
         * Returns all players that aren't the current player.
         * You can get all opponent fleets with [fleet for fleet in player.fleets for player in board.opponents]
         */
        get: function () {
            var _this = this;
            return this.players.filter(function (player) { return player.id != _this.currentPlayerId; });
        },
        enumerable: false,
        configurable: true
    });
    Board.prototype.createUid = function () {
        this.uidCounter += 1;
        return "".concat(this.step + 1, "-").concat(this.uidCounter - 1);
    };
    Board.prototype.isValidFlightPlan = function (flightPlan) {
        var allowed = "NESWC0123456789";
        var matches = 0;
        for (var i = 0; i < flightPlan.length; i++) {
            var c = flightPlan.substring(i, i + 1);
            if (allowed.indexOf(c) === -1) {
                return false;
            }
        }
        return true;
    };
    Board.prototype.findFirstNonDigit = function (candidateStr) {
        if (candidateStr.length == 0)
            return 0;
        for (var i = 0; i < candidateStr.length; i++) {
            if (isNaN(Number(candidateStr.charAt(i)))) {
                return i;
            }
        }
        return candidateStr.length + 1;
    };
    Board.prototype.combineFleets = function (board, fid1, fid2) {
        var f1 = board.fleets.get(fid1);
        var f2 = board.fleets.get(fid2);
        if (f1.lessThanOtherAlliedFleet(f2)) {
            var temp = f1;
            f1 = f2;
            f2 = temp;
            var tempS = fid1;
            fid1 = fid2;
            fid2 = tempS;
        }
        f1.kore += f2.kore;
        f1.shipCount += f2.shipCount;
        board.deleteFleet(f2);
        return fid1;
    };
    /**
     * Accepts the list of fleets at a particular position (must not be empty).
     * Returns the fleet with the most ships or None in the case of a tie along with all other fleets.
     */
    Board.prototype.resolveCollision = function (fleets) {
        if (fleets.length == 1) {
            return new Pair_1.Pair(fleets[0], []);
        }
        var fleetsByShips = new Map();
        for (var _i = 0, fleets_1 = fleets; _i < fleets_1.length; _i++) {
            var fleet = fleets_1[_i];
            var ships = fleet.shipCount;
            if (!fleetsByShips.has(ships)) {
                fleetsByShips.set(ships, []);
            }
            fleetsByShips.get(ships).push(fleet);
        }
        var mostShips = Math.max.apply(Math, Array.from(fleetsByShips.keys()));
        var largestFleets = fleetsByShips.get(mostShips);
        if (largestFleets.length == 1) {
            // There was a winner, return it
            var winner_1 = largestFleets[0];
            return new Pair_1.Pair(winner_1, fleets.filter(function (f) { return !(f.id == winner_1.id); }));
        }
        // There was a tie for most ships, all are deleted
        return new Pair_1.Pair(undefined, fleets);
    };
    /**
     * Returns a new board with the current board's next actions applied.
     * The current board is unmodified.
     * This can form a kore interpreter, e.g.
     *     next_observation = Board(current_observation, configuration, actions).next().observation
     */
    Board.prototype.next = function () {
        var _this = this;
        // Create a copy of the board to modify so we don't affect the current board
        var board = this.cloneBoard();
        var configuration = board.configuration;
        var converstCost = configuration.convertCost;
        var spawnCost = configuration.spawnCost;
        this.uidCounter = 0;
        // Process actions and store the results in the fleets and shipyards lists for collision checking
        for (var _i = 0, _a = board.players; _i < _a.length; _i++) {
            var player = _a[_i];
            // shipyard actions
            for (var _b = 0, _c = player.shipyards; _b < _c.length; _b++) {
                var shipyard = _c[_b];
                if (!shipyard.nextAction) {
                    continue;
                }
                var nextAction = shipyard.nextAction;
                if (nextAction.shipCount == 0) {
                    continue;
                }
                if (nextAction.actionType == ShipyardAction_1.ShipyardAction.SPAWN && player.kore >= spawnCost * nextAction.shipCount && nextAction.shipCount <= shipyard.maxSpawn) {
                    player.kore -= spawnCost * nextAction.shipCount;
                    shipyard.shipCount += nextAction.shipCount;
                }
                else if (nextAction.actionType == ShipyardAction_1.ShipyardAction.LAUNCH && shipyard.shipCount >= nextAction.shipCount) {
                    var flightPlan = nextAction.flightPlan;
                    if (flightPlan.length == 0 || !this.isValidFlightPlan(flightPlan)) {
                        continue;
                    }
                    shipyard.shipCount -= nextAction.shipCount;
                    var direction = Direction_1.Direction.fromChar(flightPlan.charAt(0));
                    var maxFlightPlanLen = Fleet_1.Fleet.maxFlightPlanLenForShipCount(nextAction.shipCount);
                    if (flightPlan.length > maxFlightPlanLen) {
                        flightPlan = flightPlan.substring(0, maxFlightPlanLen);
                    }
                    board.addFleet(new Fleet_1.Fleet(this.createUid(), nextAction.shipCount, direction, shipyard.position, 0, flightPlan, player.id, board));
                }
            }
            // clear next action and increase turns controlled
            for (var _d = 0, _e = player.shipyards; _d < _e.length; _d++) {
                var shipyard = _e[_d];
                shipyard.nextAction = undefined;
                shipyard.turnsControlled += 1;
            }
            // update fleets 
            for (var _f = 0, _g = player.fleets; _f < _g.length; _f++) {
                var fleet = _g[_f];
                // remove any errant 0s
                while (fleet.flightPlan.length > 0 && fleet.flightPlan.startsWith("0")) {
                    fleet.flightPlan = fleet.flightPlan.substring(1);
                }
                if (fleet.flightPlan.length > 0 && fleet.flightPlan.startsWith("C") && fleet.shipCount >= converstCost && fleet.cell.shipyardId.length == 0) {
                    player.kore += fleet.kore;
                    fleet.cell.kore = 0;
                    board.addShipyard(new Shipyard_1.Shipyard(this.createUid(), fleet.shipCount - converstCost, fleet.position, player.id, 0, board, undefined));
                    board.deleteFleet(fleet);
                    continue;
                }
                else if (fleet.flightPlan.length > 0 && fleet.flightPlan.startsWith("C")) {
                    // couldn't build, remove the Convert and continue with flight plan
                    fleet.flightPlan = fleet.flightPlan.substring(1);
                }
                if (fleet.flightPlan.length > 0 && "NESW".indexOf(fleet.flightPlan.charAt(0)) > -1) {
                    fleet.direction = Direction_1.Direction.fromChar(fleet.flightPlan.charAt(0));
                    fleet.flightPlan = fleet.flightPlan.substring(1);
                }
                else if (fleet.flightPlan.length > 0) {
                    var idx = this.findFirstNonDigit(fleet.flightPlan);
                    var digits = parseInt(fleet.flightPlan.substring(0, idx));
                    var rest = fleet.flightPlan.substring(idx);
                    digits -= 1;
                    if (digits > 0) {
                        fleet.flightPlan = digits.toString() + rest;
                    }
                    else {
                        fleet.flightPlan = rest;
                    }
                }
                // continue moving in the fleet's direction
                fleet.cell.fleetId = "";
                fleet.position = fleet.position.translate(fleet.direction, configuration.size);
                // We don't set the new cell's fleet_id here as it would be overwritten by another fleet in the case of collision.
            }
            var fleetsByLoc = new Map();
            for (var _h = 0, _j = player.fleets; _h < _j.length; _h++) {
                var fleet = _j[_h];
                var locIdx = fleet.position.toIndex(configuration.size);
                if (!fleetsByLoc.has(locIdx)) {
                    fleetsByLoc.set(locIdx, []);
                }
                fleetsByLoc.get(locIdx).push(fleet);
            }
            for (var _k = 0, _l = Array.from(fleetsByLoc.values()); _k < _l.length; _k++) {
                var fleets = _l[_k];
                fleets.sort(function (a, b) {
                    if (a.shipCount != b.shipCount) {
                        return a.shipCount > b.shipCount ? -1 : 1;
                    }
                    if (a.kore != b.kore) {
                        return a.kore > b.kore ? -1 : 1;
                    }
                    return a.direction.toIndex() > a.direction.toIndex() ? 1 : -1;
                });
                var fid = fleets[0].id;
                for (var i = 1; i < fleets.length; i++) {
                    fid = this.combineFleets(board, fid, fleets[1].id);
                }
            }
        }
        // Check for fleet to fleet collisions
        var fleetCollisionGroups = new Map();
        board.fleets.forEach(function (fleet) {
            var posIdx = fleet.position.toIndex(board.size);
            if (!fleetCollisionGroups.has(posIdx)) {
                fleetCollisionGroups.set(posIdx, [fleet]);
            }
            else {
                fleetCollisionGroups.get(posIdx).push(fleet);
            }
        });
        fleetCollisionGroups.forEach(function (collidedFleets, positionIdx) {
            var position = Point_1.Point.fromIndex(positionIdx, configuration.size);
            var pair = _this.resolveCollision(collidedFleets);
            var winnerOptional = pair.first;
            var deleted = pair.second;
            var shipyardOpt = board.getShipyardAtPoint(position);
            if (winnerOptional) {
                var winner = winnerOptional;
                winner.cell.fleetId = winner.id;
                var maxEnemySize = deleted.length > 0 ? deleted.map(function (f) { return f.shipCount; }).reduce(function (a, b) { return a > b ? a : b; }, 0) : 0;
                winner.shipCount -= maxEnemySize;
            }
            for (var _i = 0, deleted_1 = deleted; _i < deleted_1.length; _i++) {
                var fleet = deleted_1[_i];
                board.deleteFleet(fleet);
                if (winnerOptional) {
                    // Winner takes deleted fleets' kore
                    winnerOptional.kore += fleet.kore;
                }
                else if (!winnerOptional && shipyardOpt) {
                    // Desposit the kore into the shipyard
                    shipyardOpt.player.kore += fleet.kore;
                }
                else if (!winnerOptional) {
                    // Desposit the kore on the square
                    board.getCellAtPosition(position).kore += fleet.kore;
                }
            }
        });
        // Check for fleet to shipyard collisions
        for (var _m = 0, _o = Array.from(board.shipyards.values()); _m < _o.length; _m++) {
            var shipyard = _o[_m];
            var optFleet = shipyard.cell.fleet;
            if (optFleet && optFleet.playerId != shipyard.playerId) {
                var fleet = optFleet;
                if (fleet.shipCount > shipyard.shipCount) {
                    var count = fleet.shipCount - shipyard.shipCount;
                    board.deleteShipyard(shipyard);
                    board.addShipyard(new Shipyard_1.Shipyard(this.createUid(), count, shipyard.position, fleet.player.id, 1, board, undefined));
                    fleet.player.kore += fleet.kore;
                    board.deleteFleet(fleet);
                }
                else {
                    shipyard.shipCount -= fleet.shipCount;
                    shipyard.player.kore += fleet.kore;
                    board.deleteFleet(fleet);
                }
            }
        }
        // Deposit kore from fleets into shipyards
        for (var _p = 0, _q = Array.from(board.shipyards.values()); _p < _q.length; _p++) {
            var shipyard = _q[_p];
            var optFleet = shipyard.cell.fleet;
            if (optFleet && optFleet.playerId == shipyard.playerId) {
                var fleet = optFleet;
                shipyard.player.kore += fleet.kore;
                shipyard.shipCount += fleet.shipCount;
                board.deleteFleet(fleet);
            }
        }
        // apply fleet to fleet damage on all orthagonally adjacent cells
        var incomingDmg = new Map();
        for (var _r = 0, _s = Array.from(board.fleets.values()); _r < _s.length; _r++) {
            var fleet = _s[_r];
            incomingDmg.set(fleet.id, 0);
            for (var _t = 0, _u = Direction_1.Direction.listDirections(); _t < _u.length; _t++) {
                var direction = _u[_t];
                var currPos = fleet.position.translate(direction, board.configuration.size);
                var optFleet = board.getFleetAtPoint(currPos);
                if (optFleet && optFleet.playerId != fleet.playerId) {
                    incomingDmg.set(fleet.id, incomingDmg.get(fleet.id) + optFleet.shipCount);
                }
            }
        }
        incomingDmg.forEach(function (damage, fleetId) {
            if (damage === 0)
                return;
            var fleet = board.fleets.get(fleetId);
            if (damage >= fleet.shipCount) {
                fleet.cell.kore += fleet.kore;
                board.deleteFleet(fleet);
            }
            else {
                fleet.shipCount -= damage;
            }
        });
        // Collect kore from cells into fleets
        for (var _v = 0, _w = Array.from(board.fleets.values()); _v < _w.length; _v++) {
            var fleet = _w[_v];
            var cell = fleet.cell;
            var deltaKore = Board.roundToThreePlaces(cell.kore * Math.min(fleet.collectionRate, .99));
            if (deltaKore > 0) {
                fleet.kore += deltaKore;
                cell.kore -= deltaKore;
            }
        }
        // Regenerate kore in cells
        for (var _x = 0, _y = board.cells; _x < _y.length; _x++) {
            var cell = _y[_x];
            if (cell.fleetId === "" && cell.shipyardId === "") {
                if (cell.kore < configuration.maxRegenCellKore) {
                    var nextKore = Board.roundToThreePlaces(cell.kore * (1 + configuration.regenRate) * 1000.0) / 1000.0;
                    cell.kore = nextKore;
                }
            }
        }
        board.step += 1;
        return board;
    };
    Board.roundToThreePlaces = function (num) {
        return Math.round(num * 1000.0) / 1000.0;
    };
    return Board;
}());
exports.Board = Board;
//# sourceMappingURL=Board.js.map