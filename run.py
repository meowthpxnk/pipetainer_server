from app import auth_service, logger, loop, server


if __name__ == "__main__":
    loop.create_task(server.serve())
    auth_service.jwt_service._set_keys()

    logger.info("Server started.")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Server prevent stopped.")
    except BaseException as err:
        logger.critical(f"Server prevent stopped. Error: {err}")
