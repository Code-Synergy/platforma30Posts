import requests
import json

# Defina sua chave da API da OpenAI
API_KEY = "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"

TEXTAO = "NOME: Jean Daniel Rosa Pires NICHO: Desenvolvimento de software, consultoria em transformação digital, soluções em automação HISTÓRIA: Minha paixão pela inovação e tecnologia sempre esteve presente na minha vida. A capacidade das tecnologias de mudar o mundo ao nosso redor sempre me fascinou. A motivação para fundar a Code Synergy foi minha curiosidade e entusiasmo. Tudo começou com um objetivo claro: ajudar as empresas a prosperarem na era digital. Aprendi que muitas empresas não conseguiram acompanhar o ritmo acelerado das inovações tecnológicas, perdendo oportunidades valiosas de crescimento e melhoria. Eu desejava mudar isso e ajudar na transformação. Nossa missão aqui na Code Synergy é criar soluções tecnológicas que não apenas resolvam problemas, mas também abram novas possibilidades. Nosso objetivo é entender profundamente os requisitos de nossos clientes e fornecer soluções personalizadas que são realmente diferenciadoras. Buscamos sempre oferecer excelência e inovação, seja por meio do desenvolvimento de software, automação de processos ou consultoria em transformação digital. Observar como nossas soluções beneficiam os negócios de nossos clientes me motiva todos os dias. É gratificante saber que estamos ajudando as empresas a crescer, aumentar a eficiência e alcançar seus objetivos com mais eficiência. Essa é a verdade por trás do trabalho que realizamos na Code Synergy. Compartilhar essa jornada com nossa audiência é uma maneira de demonstrar que um verdadeiro compromisso com a excelência e uma paixão genuína pela inovação estão por trás de todas as tecnologias que estamos oferecendo. Além disso, é essa paixão que nos motiva a continuar crescendo e oferecendo o melhor para nossos clientes. CLIENTE IDEAL: Setor: Empresas de diversos setores, incluindo tecnologia, finanças, educação, saúde e comércio. Tamanho: Pequenas, médias e grandes empresas que buscam inovação e transformação digital. Localização: Empresas localizadas em qualquer lugar, com preferência por aquelas na região de São Carlos ou com presença na mesma. Necessidades e Desafios Transformação Digital: Empresas que precisam migrar processos tradicionais para soluções digitais, melhorando a eficiência operacional e a experiência do cliente. Desenvolvimento de Software: Negócios que precisam de aplicativos personalizados, integração de sistemas ou desenvolvimento de APIs. Automação de Processos: Empresas que desejam automatizar processos empresariais para reduzir custos e aumentar a produtividade. Infraestrutura de TI: Organizações que necessitam de suporte em gestão de infraestrutura, soluções em nuvem e segurança da informação. Análise de Dados: Empresas que buscam aproveitar big data e inteligência artificial para obter insights e otimizar operações. Características Ideais Foco em Inovação: Empresas dispostas a investir em novas tecnologias e a adotar soluções inovadoras para se manterem competitivas. Crescimento e Expansão: Negócios em fase de crescimento ou expansão, que precisam de suporte tecnológico para sustentar esse crescimento. Colaboração e Parceria: Clientes que valorizam a colaboração estreita e a comunicação aberta com seus fornecedores de tecnologia. Disposição para Mudança: Empresas abertas a mudanças e adaptações, prontas para implementar melhorias contínuas em seus processos e sistemas. Exemplos de Clientes Ideais Startups de Tecnologia: Startups que precisam desenvolver seu produto mínimo viável (MVP) rapidamente e com qualidade, além de integrações e melhorias contínuas. Instituições Educacionais: Escolas e universidades que desejam implementar plataformas de gerenciamento de alunos, automação de processos administrativos e integração de soluções de aprendizado digital. Empresas de Comércio: Negócios de comércio eletrônico que buscam otimizar suas operações, melhorar a experiência do cliente e integrar soluções de pagamento e logística. Empresas de Saúde: Clínicas e hospitais que necessitam de soluções de gerenciamento de pacientes, automação de processos clínicos e integração de sistemas de saúde. Benefícios para o Cliente Soluções Personalizadas: A Code Synergy oferece soluções tecnológicas personalizadas que atendem às necessidades específicas de cada cliente. Inovação e Competitividade: Com o suporte da Code Synergy, os clientes podem adotar as mais recentes inovações tecnológicas, mantendo-se competitivos no mercado. Eficiência Operacional: A implementação de automação e outras tecnologias avançadas ajuda a melhorar a eficiência operacional, reduzindo custos e aumentando a produtividade. Suporte Contínuo: A Code Synergy fornece suporte contínuo e parceria de longo prazo, garantindo que as soluções implementadas continuem a atender às necessidades do cliente conforme elas evoluem. Em resumo, o cliente ideal para a Code Synergy é uma empresa inovadora e em crescimento, disposta a investir em transformação digital e automação, e que valoriza uma parceria colaborativa e soluções tecnológicas personalizadas para alcançar seus objetivos estratégicos. PRODUTO: Produtos e Serviços a Divulgar: Desenvolvimento de Software Personalizado Descrição: Oferecemos soluções de software sob medida para atender às necessidades específicas de cada cliente. Nosso processo inclui análise detalhada, design, desenvolvimento, testes e implementação, garantindo que o software entregue seja altamente funcional e alinhado com os objetivos do negócio. Consultoria em Transformação Digital Descrição: Ajudamos empresas a se adaptarem à era digital, revisando processos e implementando tecnologias avançadas para melhorar a eficiência e a competitividade. Nossos serviços incluem avaliação de necessidades, planejamento estratégico e suporte contínuo na adoção de novas tecnologias. Automação de Processos Empresariais Descrição: Implementamos soluções de automação, como RPA (Robotic Process Automation) e integração de IA, para otimizar processos internos, reduzir custos operacionais e aumentar a produtividade. Nossos especialistas identificam oportunidades de automação e desenvolvem fluxos de trabalho personalizados. Gestão de Infraestrutura de TI Descrição: Oferecemos serviços completos de gestão de infraestrutura de TI, incluindo monitoramento, manutenção e suporte de sistemas. Nossas soluções garantem que a infraestrutura tecnológica da empresa seja segura, eficiente e escalável, suportando o crescimento do negócio. Soluções de Segurança da Informação Descrição: Fornecemos serviços de segurança da informação para proteger dados sensíveis e sistemas contra ameaças cibernéticas. Nossas ofertas incluem avaliações de segurança, implementação de medidas de proteção, conformidade com regulamentações e resposta a incidentes. Produtos e Serviços Complementares: Desenvolvimento de APIs e Integração de Sistemas Descrição: Criamos e integramos APIs para permitir que diferentes sistemas se comuniquem de maneira eficaz. Nossas soluções de integração garantem uma troca de dados fluida e segura, melhorando a interoperabilidade e a eficiência operacional. Desenvolvimento de Plataformas de Membros/Alunos Descrição: Desenvolvemos plataformas personalizadas para gerenciar membros e alunos, com funcionalidades específicas para inscrições, pagamentos, comunicação e acompanhamento de atividades. Nossas plataformas são intuitivas e fáceis de usar, proporcionando uma excelente experiência ao usuário. Consultoria em Tecnologias Emergentes Descrição: Oferecemos consultoria especializada em tecnologias emergentes, como blockchain, IoT (Internet das Coisas) e inteligência artificial. Ajudamos as empresas a entender e implementar essas tecnologias para inovar e se destacar no mercado. Serviços de Cloud Computing Descrição: Ajudamos empresas a migrar para a nuvem e a gerenciar seus recursos de cloud computing. Nossos serviços incluem planejamento, implementação, otimização e suporte contínuo, garantindo que as soluções em nuvem sejam seguras, escaláveis e eficientes. Desenvolvimento de Soluções de Big Data Descrição: Desenvolvemos e implementamos soluções de big data para ajudar empresas a coletar, armazenar, analisar e utilizar grandes volumes de dados. Nossas soluções permitem insights valiosos que orientam a tomada de decisões estratégicas. TEMA: Tema Principal: Inovação e Transformação Digital Temas Secundários: Tecnologias Emergentes Automação e IA Desenvolvimento de Software e Integração de Sistemas Boas Práticas em TI e Segurança da Informação Subtemas: Inovação e Transformação Digital: Casos de Sucesso: Exemplos de empresas que se transformaram digitalmente. Estratégias de Transformação: Passos práticos para a transformação digital. Benefícios e Desafios: Como superar os obstáculos e aproveitar as vantagens. Tecnologias Emergentes: Tendências Tecnológicas: Novidades e tendências no mercado de tecnologia. Blockchain: Aplicações e impactos no mercado. Internet das Coisas (IoT): Como a IoT está revolucionando diferentes setores. Automação e IA: Automação de Processos: Exemplos práticos e benefícios da automação. Inteligência Artificial: Implementação e casos de uso de IA em negócios. RPA (Robotic Process Automation): Como a RPA pode otimizar operações empresariais. Desenvolvimento de Software e Integração de Sistemas: Metodologias Ágeis: Benefícios e práticas recomendadas. APIs e Integrações: Importância da integração de sistemas e desenvolvimento de APIs robustas. Desenvolvimento Personalizado: Vantagens de soluções sob medida para empresas. Boas Práticas em TI e Segurança da Informação: Segurança Cibernética: Dicas e estratégias para proteger dados e sistemas. Gestão de Infraestrutura: Melhores práticas para gerenciar e manter a infraestrutura de TI. Compliance e Regulamentações: Conformidade com leis e normas de segurança da informação."

BASE = "A partir dos texto abaixo gerar post para midias sociais, devem ser gerados 3 posts com titulo, texto minimo 250 palavras e 5 hashtags: "

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2",
    "id": "asst_XlQl4tqzHEnlYOC49tkxRgBX"
}

data = {
    #"id": "asst_XlQl4tqzHEnlYOC49tkxRgBX",
    "model": "gpt-4o-2024-05-13",  # Atualize o modelo se necessário
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
            #{"role": "user", "content": "Estou usando a Zoe?"}
        {"role": "user", "content": BASE + TEXTAO}
    ],
    "temperature": 0.7
    #"max_tokens": 50
}

# URL correta para a API de chat completions
response = requests.post("https://api.openai.com/v1/chat/completions",
                         headers=headers, data=json.dumps(data))

# Verifique o código de status da resposta
if response.status_code == 200:
    try:
        # Tente acessar a resposta de chat
        output = response.json()['choices'][0]['message']['content']
        print(output)

        # Aqui você insere o retorno do GPT no banco de dados do serviço legendas
        legenda_data = {
            "id_form": 123,  # substitua com o valor correto
            "dia_post": "1",  # substitua com a data correta
            "ds_legenda": "Teste de isert pela ZOE auto"
        }

        # Envia a legenda para o serviço de legendas
        legendas_response = requests.post("http://localhost:5000/legendas", json=legenda_data)

        if legendas_response.status_code == 201:
            print("Legenda gravada com sucesso!")
        else:
            print(f"Erro ao gravar legenda: {legendas_response.status_code}")
            print(legendas_response.text)





    except KeyError:
        # Imprima a resposta completa se 'choices' não estiver presente
        print("Erro: 'choices' não encontrado na resposta.")
        print(response.json())
else:
    print(f"Erro: A requisição falhou com o código de status {response.status_code}")
    print(response.text)
