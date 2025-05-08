import asyncio
from agents import Runner

from .project_architect import project_architect
from .model_agent import model_agent
from .view_agent import view_agent
from .template_agent import template_agent
from .url_agent import url_agent
from .scaffold import scaffold_agent
from .agent_models import DjangoProjectPlan, ModelsOutput, TemplatesOutput, ViewOutput, UrlsOutput
from .logging_config import setup_logger

logger = setup_logger()


async def main(idea, prompt_id):
    # idea = input("Describe your Django project idea: ")
    logger.info("Starting project architecture ...")
    result = await Runner.run(project_architect, idea)
    logger.info("Finished project architecture...")
    logger.debug(result)
    django_project_plan = result.final_output_as(DjangoProjectPlan)
    logger.debug(django_project_plan)

    logger.info("Starting model creation ...")
    result = await Runner.run(
        starting_agent=model_agent,
        input=f"From the context that you have create the django models please {django_project_plan}",
    )
    logger.info("Finished model creation ...")
    logger.debug("\nGenerated Models:")
    logger.debug(result)
    models_output = result.final_output_as(ModelsOutput)
    logger.debug(models_output)
    logger.info("Starting view creation ...")
    result = await Runner.run(
        starting_agent=view_agent,
        input=f"From the context that you have create the django views please {models_output} app structure {django_project_plan}",
    )
    logger.info("Finished view creation ...")
    logger.debug(result)
    view_output = result.final_output_as(ViewOutput)
    logger.debug(view_output)

    
    logger.info("Starting template creation ...")
    result = await Runner.run(
        starting_agent=template_agent,
        input=f"From the context that you have create the django templates please {models_output} app structure {django_project_plan} views {view_output}",
    )
    logger.info("Finished template creation ...")
    logger.debug(result)
    templates_output = result.final_output_as(TemplatesOutput)
    logger.debug(templates_output)

    
    logger.info("Starting url creation ...")
    result = await Runner.run(
        starting_agent=url_agent,
        input=f"From the context that you have create the django urls please {models_output} app structure {django_project_plan} views {view_output}, templates {templates_output}",
    )
    logger.info("Finished url creation ...")
    logger.debug(result)
    urls_output = result.final_output_as(UrlsOutput)
    logger.debug(urls_output)


    logger.info("Starting project realisation ...")
    result = await Runner.run(
        starting_agent=scaffold_agent,
        input=f"From the context that you have create the django project please {models_output} app structure {django_project_plan} views {view_output}, templates {templates_output}, urls {urls_output} create it into destination \"project_{prompt_id}\"",
    )
    logger.info("Finished project realisation ...")
    logger.debug(result)
    
if __name__ == "__main__":
    asyncio.run(main())
