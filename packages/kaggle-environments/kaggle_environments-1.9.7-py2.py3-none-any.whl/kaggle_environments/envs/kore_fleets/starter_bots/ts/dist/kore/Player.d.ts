import { Board } from "./Board";
import { Fleet } from "./Fleet";
import { Shipyard } from "./Shipyard";
import { ShipyardAction } from "./ShipyardAction";
export declare class Player {
    readonly id: number;
    kore: number;
    readonly shipyardIds: string[];
    readonly fleetIds: string[];
    readonly board: Board;
    constructor(playerId: number, kore: number, shipyardIds: string[], fleetIds: string[], board: Board);
    cloneToBoard(board: Board): Player;
    /**
     * Returns all shipyards owned by this player.
     * @return
     */
    get shipyards(): Shipyard[];
    /**
     * Returns all fleets owned by this player.
     */
    get fleets(): Fleet[];
    /**
     * Returns whether this player is the current player (generally if this returns True, this player is you.
     */
    isCurrentPlayer(): boolean;
    /**
     * Returns all queued fleet and shipyard actions for this player formatted for the kore interpreter to receive as an agent response.
     */
    get nextActions(): Map<String, ShipyardAction>;
    /**
     * Converts a player back to the normalized observation subset that constructed it.
     */
    observation(): any[];
}
