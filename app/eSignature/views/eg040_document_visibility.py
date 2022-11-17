"""Example 040: Document Visibility"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint, session

from ..examples.eg040_document_visibility import Eg040DocumentVisibility
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

example_number = 40
eg = f"eg0{example_number}"  # reference (and url) for this example
eg040 = Blueprint(eg, __name__)


@eg040.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def embedded_signing():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """
    example = get_example_by_number(session["manifest"], example_number)

    try:
        # 1. Get required arguments
        args = Eg040DocumentVisibility.get_args()
        # 2. Call the worker method
        results = Eg040DocumentVisibility.worker(args, DS_CONFIG["doc_docx"], DS_CONFIG["doc_pdf"])
    except ApiException as err:
        return process_error(err)

    # 3. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"The envelope has been created and sent!<br/>Envelope ID {results['envelope_id']}."
    )

@eg040.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    if "is_cfr" in session and session["is_cfr"] == "enabled":
        return render_template("cfr_error.html", title="Error")

    return render_template(
        "eg040_document_visibility.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg040_document_visibility.py",
        source_url=DS_CONFIG["github_example_url"] + "eg040_document_visibility.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer1_name=DS_CONFIG["signer_name"],
        signer1_email=DS_CONFIG["signer_email"]
    )
