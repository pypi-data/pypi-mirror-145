"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var mocha_1 = require("mocha");
var chai_1 = require("chai");
var fs = __importStar(require("fs"));
var Board_1 = require("../kore/Board");
var Direction_1 = require("../kore/Direction");
var Point_1 = require("../kore/Point");
var Fleet_1 = require("../kore/Fleet");
var Shipyard_1 = require("../kore/Shipyard");
var ShipyardAction_1 = require("../kore/ShipyardAction");
var getStarterBoard = function () {
    var rawConfig = fs.readFileSync('./test/configuration.json', 'utf8');
    var rawObs = fs.readFileSync('./test/observation.json', 'utf8');
    return Board_1.Board.fromRaw(rawObs, rawConfig);
};
(0, mocha_1.describe)('Board', function () {
    it('init works correctly', function () {
        var rawConfig = fs.readFileSync('./test/configuration.json', 'utf8');
        var rawObs = fs.readFileSync('./test/observation.json', 'utf8');
        var board = Board_1.Board.fromRaw(rawObs, rawConfig);
        (0, chai_1.expect)(board.step).to.equal(16);
    });
    (0, mocha_1.describe)('kore', function () {
        it('regenerates', function () {
            var board = getStarterBoard();
            var nextBoard = board.next();
            (0, chai_1.expect)(board.cells[3].kore).to.be.lessThan(nextBoard.cells[3].kore);
        });
        it('is picked up by fleets', function () {
            var board = getStarterBoard();
            var p = new Point_1.Point(10, 10);
            board.getCellAtPosition(p).kore = 100;
            board.getCellAtPosition(p.add(Direction_1.Direction.SOUTH)).kore = 100;
            var fleet = new Fleet_1.Fleet("test-fleet", 100, Direction_1.Direction.SOUTH, p, 100.0, "8N", 0, board);
            board.addFleet(fleet);
            var nextBoard = board.next();
            var nextFleet = nextBoard.getFleetAtPoint(p.add(Direction_1.Direction.SOUTH));
            (0, chai_1.expect)(nextFleet.kore).to.be.greaterThan(fleet.kore);
        });
    });
    (0, mocha_1.describe)('spawnShips', function () {
        it('spawnsShips', function () {
            var board = getStarterBoard();
            var shipyardId = board.players[0].shipyardIds[0];
            var shipyard = board.shipyards.get(shipyardId);
            shipyard.setNextAction(ShipyardAction_1.ShipyardAction.spawnShips(1));
            var nextBoard = board.next();
            var nextShipyard = nextBoard.shipyards.get(shipyardId);
            (0, chai_1.expect)(shipyard.shipCount).to.equal(0);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(1);
        });
        it('can spawn 0 ships', function () {
            var board = getStarterBoard();
            var shipyardId = board.players[0].shipyardIds[0];
            var shipyard = board.shipyards.get(shipyardId);
            shipyard.setNextAction(ShipyardAction_1.ShipyardAction.spawnShips(0));
            var nextBoard = board.next();
            var nextShipyard = nextBoard.shipyards.get(shipyardId);
            (0, chai_1.expect)(shipyard.shipCount).to.equal(0);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(0);
        });
    });
    (0, mocha_1.describe)('launchShips', function () {
        it('launches', function () {
            var board = getStarterBoard();
            var shipyardId = board.players[0].shipyardIds[0];
            var shipyard = board.shipyards.get(shipyardId);
            shipyard.shipCount = 100;
            shipyard.setNextAction(ShipyardAction_1.ShipyardAction.launchFleetWithFlightPlan(10, "N"));
            var nextBoard = board.next();
            var nextShipyard = nextBoard.shipyards.get(shipyardId);
            var launchedFleet = nextBoard.getFleetAtPoint(shipyard.position.add(Direction_1.Direction.NORTH));
            (0, chai_1.expect)(shipyard.shipCount).to.equal(100);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(90);
            (0, chai_1.expect)(!!launchedFleet).to.be.true;
            (0, chai_1.expect)(launchedFleet.shipCount).to.equal(10);
        });
        it('can spawn 0 ships', function () {
            var board = getStarterBoard();
            var shipyardId = board.players[0].shipyardIds[0];
            var shipyard = board.shipyards.get(shipyardId);
            shipyard.setNextAction(ShipyardAction_1.ShipyardAction.spawnShips(0));
            var nextBoard = board.next();
            var nextShipyard = nextBoard.shipyards.get(shipyardId);
            (0, chai_1.expect)(shipyard.shipCount).to.equal(0);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(0);
        });
    });
    (0, mocha_1.describe)('flight plan', function () {
        it('decrements', function () {
            var board = getStarterBoard();
            var p = new Point_1.Point(10, 11);
            var f = new Fleet_1.Fleet("test-fleet", 10, Direction_1.Direction.SOUTH, p, 100.0, "8N", 0, board);
            board.addFleet(f);
            var nextBoard = board.next();
            var nextFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(nextFleet.direction.toChar()).to.equal(Direction_1.Direction.SOUTH.toChar());
            (0, chai_1.expect)(nextFleet.flightPlan).to.equal("7N");
        });
        it('changed direction', function () {
            var board = getStarterBoard();
            var p = new Point_1.Point(10, 11);
            var f = new Fleet_1.Fleet("test-fleet", 10, Direction_1.Direction.NORTH, p, 100.0, "S", 0, board);
            board.addFleet(f);
            var nextBoard = board.next();
            var nextFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(nextFleet.direction.toChar()).to.equal(Direction_1.Direction.SOUTH.toChar());
            (0, chai_1.expect)(nextFleet.flightPlan).to.equal("");
        });
        it('converts to shipyard', function () {
            var board = getStarterBoard();
            var p = new Point_1.Point(10, 11);
            var f = new Fleet_1.Fleet("test-fleet", 10, Direction_1.Direction.SOUTH, p, 100.0, "C", 0, board);
            board.addFleet(f);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p)).to.be.false;
            var nextFleet = nextBoard.getFleetAtPoint(p.add(Direction_1.Direction.SOUTH));
            (0, chai_1.expect)(nextFleet.playerId).to.equal(0);
            (0, chai_1.expect)(nextFleet.shipCount).to.equal(10);
            (0, chai_1.expect)(nextFleet.direction.toChar()).to.equal(Direction_1.Direction.SOUTH.toChar());
        });
        it('does not convert to shipyard if not enough ships', function () {
            var board = getStarterBoard();
            var p = new Point_1.Point(10, 11);
            var f = new Fleet_1.Fleet("test-fleet", 100, Direction_1.Direction.NORTH, p, 100.0, "C", 0, board);
            board.addFleet(f);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p)).to.be.true;
            var nextShipyard = nextBoard.getShipyardAtPoint(p);
            (0, chai_1.expect)(nextShipyard.playerId).to.equal(0);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(50);
        });
    });
    (0, mocha_1.describe)('coalescence', function () {
        it('correctly joins allied fleets', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 11, Direction_1.Direction.NORTH, p2, 100.0, "", 0, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            var combinedFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(combinedFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(combinedFleet.shipCount).to.equal(21);
        });
        it('joins on first tie break', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 10, Direction_1.Direction.NORTH, p2, 101.0, "10S", 0, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            var combinedFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(combinedFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(combinedFleet.shipCount).to.equal(20);
            (0, chai_1.expect)(combinedFleet.flightPlan).to.equal("9S");
        });
        it('joins on second tie break', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 10, Direction_1.Direction.NORTH, p2, 100.0, "", 0, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            var combinedFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(combinedFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(combinedFleet.shipCount).to.equal(20);
        });
    });
    (0, mocha_1.describe)('fleet battles', function () {
        it('resolve correctly with a winner', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(9, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 11, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(new Point_1.Point(10, 10))).to.be.true;
            var survivingFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(survivingFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(survivingFleet.shipCount).to.equal(1);
            (0, chai_1.expect)(survivingFleet.playerId).to.equal(1);
        });
        it('resolve correctly with a tie', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(9, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 10, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            var collision = new Point_1.Point(10, 10);
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(collision)).to.be.false;
            (0, chai_1.expect)(board.getCellAtPosition(collision).kore + 100).to.be.lessThan(nextBoard.getCellAtPosition(collision).kore);
        });
    });
    (0, mocha_1.describe)('fleet collisions', function () {
        it('resolve correctly with a winner', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 11, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(new Point_1.Point(10, 10))).to.be.true;
            var survivingFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(survivingFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(survivingFleet.shipCount).to.equal(1);
            (0, chai_1.expect)(survivingFleet.playerId).to.equal(1);
        });
        it('resolve correctly with multiples from one player', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var p3 = new Point_1.Point(9, 10);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 11, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            var f3 = new Fleet_1.Fleet("f3", 2, Direction_1.Direction.EAST, p3, 100.0, "", 0, board);
            board.addFleet(f1);
            board.addFleet(f2);
            board.addFleet(f3);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(new Point_1.Point(10, 10))).to.be.true;
            var survivingFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(survivingFleet.direction.toChar()).to.equal(Direction_1.Direction.SOUTH.toChar());
            (0, chai_1.expect)(survivingFleet.shipCount).to.equal(1);
            (0, chai_1.expect)(survivingFleet.playerId).to.equal(0);
        });
        it('resolve correctly with multiples players', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var p3 = new Point_1.Point(9, 10);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 11, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            var f3 = new Fleet_1.Fleet("f3", 2, Direction_1.Direction.EAST, p3, 100.0, "", 2, board);
            board.addFleet(f1);
            board.addFleet(f2);
            board.addFleet(f3);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(new Point_1.Point(10, 10))).to.be.true;
            var survivingFleet = nextBoard.getFleetAtPoint(new Point_1.Point(10, 10));
            (0, chai_1.expect)(survivingFleet.direction.toChar()).to.equal(Direction_1.Direction.NORTH.toChar());
            (0, chai_1.expect)(survivingFleet.shipCount).to.equal(1);
            (0, chai_1.expect)(survivingFleet.playerId).to.equal(1);
        });
        it('resolve correctly with a tie', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 9);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var f2 = new Fleet_1.Fleet("f2", 10, Direction_1.Direction.NORTH, p2, 100.0, "", 1, board);
            board.addFleet(f1);
            board.addFleet(f2);
            var nextBoard = board.next();
            var collision = new Point_1.Point(10, 10);
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(new Point_1.Point(10, 10))).to.be.false;
            (0, chai_1.expect)(board.getCellAtPosition(collision).kore + 100).to.be.lessThan(nextBoard.getCellAtPosition(collision).kore);
        });
    });
    (0, mocha_1.describe)('fleet/shipyard collisions', function () {
        it('works when they are allied', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 10);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 0, board);
            var s1 = new Shipyard_1.Shipyard("s1", 0, p2, 0, 100, board, null);
            board.addFleet(f1);
            board.addShipyard(s1);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(p2)).to.be.false;
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p2)).to.be.true;
            var nextShipyard = nextBoard.getShipyardAtPoint(p2);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(10);
            (0, chai_1.expect)(nextShipyard.playerId).to.equal(0);
            (0, chai_1.expect)(s1.turnsControlled).to.equal(100);
            (0, chai_1.expect)(nextShipyard.turnsControlled).to.equal(101);
            (0, chai_1.expect)(nextBoard.players[0].kore).to.equal(board.players[0].kore + 100);
        });
        it('smaller fleet does not take over larger shipyard', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 10);
            var f1 = new Fleet_1.Fleet("f1", 10, Direction_1.Direction.SOUTH, p1, 100.0, "", 1, board);
            var s1 = new Shipyard_1.Shipyard("s1", 100, p2, 0, 100, board, null);
            board.addFleet(f1);
            board.addShipyard(s1);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(p2)).to.be.false;
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p2)).to.be.true;
            var nextShipyard = nextBoard.getShipyardAtPoint(p2);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(90);
            (0, chai_1.expect)(nextShipyard.playerId).to.equal(0);
            (0, chai_1.expect)(s1.turnsControlled).to.equal(100);
            (0, chai_1.expect)(nextShipyard.turnsControlled).to.equal(101);
            (0, chai_1.expect)(nextBoard.players[0].kore).to.equal(board.players[0].kore + 100);
        });
        it('equal fleet does not take over larger shipyard', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 10);
            var f1 = new Fleet_1.Fleet("f1", 100, Direction_1.Direction.SOUTH, p1, 100.0, "", 1, board);
            var s1 = new Shipyard_1.Shipyard("s1", 100, p2, 0, 100, board, null);
            board.addFleet(f1);
            board.addShipyard(s1);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(p2)).to.be.false;
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p2)).to.be.true;
            var nextShipyard = nextBoard.getShipyardAtPoint(p2);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(0);
            (0, chai_1.expect)(nextShipyard.playerId).to.equal(0);
            (0, chai_1.expect)(s1.turnsControlled).to.equal(100);
            (0, chai_1.expect)(nextShipyard.turnsControlled).to.equal(101);
            (0, chai_1.expect)(nextBoard.players[0].kore).to.equal(board.players[0].kore + 100);
        });
        it('larger fleet does take over smaller shipyard', function () {
            var board = getStarterBoard();
            var p1 = new Point_1.Point(10, 11);
            var p2 = new Point_1.Point(10, 10);
            var f1 = new Fleet_1.Fleet("f1", 110, Direction_1.Direction.SOUTH, p1, 100.0, "", 1, board);
            var s1 = new Shipyard_1.Shipyard("s1", 100, p2, 0, 100, board, null);
            board.addFleet(f1);
            board.addShipyard(s1);
            var nextBoard = board.next();
            (0, chai_1.expect)(!!nextBoard.getFleetAtPoint(p2)).to.be.false;
            (0, chai_1.expect)(!!nextBoard.getShipyardAtPoint(p2)).to.be.true;
            var nextShipyard = nextBoard.getShipyardAtPoint(p2);
            (0, chai_1.expect)(nextShipyard.shipCount).to.equal(10);
            (0, chai_1.expect)(nextShipyard.playerId).to.equal(1);
            (0, chai_1.expect)(s1.turnsControlled).to.equal(100);
            (0, chai_1.expect)(nextShipyard.turnsControlled).to.equal(1);
            (0, chai_1.expect)(nextBoard.players[1].kore).to.equal(board.players[1].kore + 100);
        });
    });
});
//# sourceMappingURL=BoardTest.js.map