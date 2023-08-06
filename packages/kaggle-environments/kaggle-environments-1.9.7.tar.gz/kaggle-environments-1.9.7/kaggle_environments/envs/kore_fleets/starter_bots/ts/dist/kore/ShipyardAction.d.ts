export declare class ShipyardAction {
    static readonly SPAWN = "SPAWN";
    static readonly LAUNCH = "LAUNCH";
    readonly actionType: string;
    readonly shipCount: number;
    readonly flightPlan: string;
    static spawnShips(shipCount: number): ShipyardAction;
    static launchFleetWithFlightPlan(shipCount: number, flightPlan: string): ShipyardAction;
    static fromstring(raw: string): ShipyardAction;
    constructor(type: string, shipCount: number, flightPlan: string);
    private get isSpawn();
    private get isLaunch();
    toString(): string;
}
