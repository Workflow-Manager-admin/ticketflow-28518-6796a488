#!/bin/bash
cd /home/kavia/workspace/code-generation/ticketflow-28518-6796a488/ticketing_frontend_workspace/ticketing_frontend
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

