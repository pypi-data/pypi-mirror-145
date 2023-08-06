import { Cell } from "./Cell";
import { Configuration } from "./Configuration";
import { Fleet } from "./Fleet";
import { Pair } from "./Pair";
import { Player } from "./Player";
import { Point } from "./Point";
import { Shipyard } from "./Shipyard";
export declare class Board {
    readonly shipyards: Map<string, Shipyard>;
    readonly fleets: Map<string, Fleet>;
    readonly players: Player[];
    readonly currentPlayerId: number;
    readonly configuration: Configuration;
    step: number;
    readonly remainingOverageTime: number;
    readonly cells: Cell[];
    readonly size: number;
    private uidCounter;
    private constructor();
    cloneBoard(): Board;
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
    static fromRaw(rawObservation: string, rawConfiguration: string): Board;
    getCellAtPosition(position: Point): Cell;
    addFleet(fleet: Fleet): void;
    addShipyard(shipyard: Shipyard): void;
    deleteFleet(fleet: Fleet): void;
    deleteShipyard(shipyard: Shipyard): void;
    getFleetAtPoint(position: Point): Fleet | undefined;
    getShipyardAtPoint(position: Point): Shipyard | undefined;
    /**
     * Returns the current player (generally this is you).
     * @return
     */
    get currentPlayer(): Player;
    /**
     * Returns all players that aren't the current player.
     * You can get all opponent fleets with [fleet for fleet in player.fleets for player in board.opponents]
     */
    get opponents(): Player[];
    private createUid;
    private isValidFlightPlan;
    private findFirstNonDigit;
    private combineFleets;
    /**
     * Accepts the list of fleets at a particular position (must not be empty).
     * Returns the fleet with the most ships or None in the case of a tie along with all other fleets.
     */
    resolveCollision(fleets: Fleet[]): Pair<(Fleet | undefined), Fleet[]>;
    /**
     * Returns a new board with the current board's next actions applied.
     * The current board is unmodified.
     * This can form a kore interpreter, e.g.
     *     next_observation = Board(current_observation, configuration, actions).next().observation
     */
    next(): Board;
    private static roundToThreePlaces;
}
