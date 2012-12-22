/*
 * Lobbypy
 *
 * Namespace: /lobby/
 * create(lobby_item_info)
 * - Create event for lobby listing
 * - Parameters:
 *   - lobby_item_info (see schema)
 * update(lobby_item_info)
 * - Update event for lobby listing
 * - Parameters:
 *   - lobby_item_info (see schema)
 * delete(lobby_id)
 * - Delete event for lobby listing
 * - Parameters:
 *   - lobby_id:
 *     - id of lobby deleted
 *
 * Namespace: /lobby/<lobby_id>
 * update(lobby_info)
 * - Update event for lobby
 * - Parameters:
 *   - lobby_info (see schema)
 * leave()
 * - Leave event for lobby.  Player has left lobby and will not
 *   recieve any more updates for the lobby.
 * delete()
 * - Delete event for lobby.  Lobby has been deleted.
 */
